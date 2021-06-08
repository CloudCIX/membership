# stdlib
from uuid import uuid4
import json
import logging
from typing import Dict
# libs
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework.request import Request
# local
from membership.models import EmailConfirmation


class EmailConfirmationEmail():  # pragma: no cover
    """
    When a public user is created, an email will be sent asking them to confirm their email
    """

    def send(self, request: Request, user: Dict, to: str, update=False):
        """
        user: serialized user data
        to: email address to send email to
        update: if True, the update_email_confirmation email will be sent
        """
        logger = logging.getLogger('membership.notifications.send')
        tracer = settings.TRACER

        with tracer.start_span('create_email_confirmation_token', child_of=request.span):
            token = EmailConfirmation(
                pk=uuid4().hex,
                data=json.dumps(user, cls=DjangoJSONEncoder),
            )
            while True:
                try:
                    token.validate_unique()
                    token.save()
                    break
                except ValidationError:
                    token.pk = uuid4().hex

        with tracer.start_span('settings_testing', child_of=request.span):
            if settings.TESTING:
                return None

        tracer = settings.TRACER
        with tracer.start_span('sending_email', child_of=request.span):
            if settings.PRODUCTION_DEPLOYMENT:
                email_to = [f'{user["first_name"]} {user["surname"]} <{user["email"]}>']
            else:
                email_to = settings.DEVELOPER_EMAILS

            email_template = 'update_email_confirmation' if update else 'email_confirmation'

            body_txt, body_html = [
                render_to_string(
                    f'email/{email_template}.{version}',
                    context={
                        'user': user,
                        'confirmation_url': settings.EMAIL_CONFIRMATION_URL + token.pk,
                        'current_email': to,
                        'request': request,
                    },
                ) for version in ['txt', 'html']
            ]

            email = EmailMultiAlternatives(
                from_email=settings.EMAIL_HOST_USER,
                to=email_to,
                subject=f'{settings.ORGANIZATION_URL} Membership Email Confirmation',
                body=body_txt,
            )
            email.attach_alternative(body_html, 'text/html')
            try:
                email.send()
            except Exception as e:
                logger.error(
                    f'Error occurred when sending confirmation email to {to} for User ID {user["id"]};',
                    f'Error: {e}',
                )
            return None
