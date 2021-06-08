"""
Confirm users emails
"""
# stdlib
from datetime import datetime
from dateutils import relativedelta
# libs
from cloudcix_rest.exceptions import Http400
from cloudcix_rest.views import APIView
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
# local
from membership.models import EmailConfirmation, User


class EmailConfirmationResource(APIView):

    def get(self, request: Request, email_token) -> Response:
        """
        summary: Check a users email confirmation token and update if valid

        description: |
            Update a user to show their email has been confirmed if their token is valid

        path_params:
            email_token:
                description: The id of the token used in confirmation
                type: str

        responses:
            200:
                description: User email confirmed successfully
            400: {}
        """
        hrs24 = datetime.now() - relativedelta(hours=24)
        try:
            token_data = EmailConfirmation.objects.get(
                pk=email_token,
                timestamp__gte=hrs24,
            )
        except EmailConfirmation.DoesNotExist:
            return Http400(error_code='membership_email_confirmation_read_001')
        user = token_data.get_user()
        # read the person, confirm username matches
        try:
            obj = User.objects.get(pk=user['id'])
        except User.DoesNotExist:
            return Http400(error_code='membership_email_confirmation_read_002')
        if obj.email != user['email']:
            return Http400(error_code='membership_email_confirmation_read_003')
        # update the person to be validated
        obj.email_validated = True
        obj.save()
        # delete token
        token_data.delete()
        return Response(status=status.HTTP_200_OK)
