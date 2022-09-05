# stdlib
from collections import deque
from datetime import datetime, timedelta
from io import TextIOBase
from smtplib import SMTPException
from typing import Deque
# lib
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.mail.backends.smtp import EmailBackend
from django.core.management.base import BaseCommand
from django.db.models import Prefetch, F
from django.template.loader import render_to_string
# local
from membership.models import Member, MemberLink, User


class ExpirationBackend(EmailBackend):
    """
    Custom email backend used to send out the expiration emails.
    Returns the success count
    """

    def send_messages(self, emails: Deque[EmailMultiAlternatives], out: TextIOBase) -> int:
        if len(emails) == 0:
            out.write('No emails to send.')
            return -1, -1
        with self._lock:
            conn = self.open()
            if self.connection is None:
                # We failed silently on open, log and cancel
                out.write('Connection failed.')
                return -1, -1
            successes = 0
            for email in emails:
                try:
                    sent = self._send(email)
                    if sent:
                        successes += 1
                except SMTPException as e:
                    out.write('Error sending message')
                    out.write(f'To: {", ".join(email.recipients)}')
                    out.write(f'Exception: {e}')
                    out.write('-' * 50)
            if conn:
                self.close()
        return successes


class Command(BaseCommand):
    """
    Send email to warn Users about upcoming expiration dates

    Users are sent warnings when their expiry date is 30 days away
    """
    help = 'Send email to warn Users about upcoming expirations'
    can_import_settings = True

    def handle(self, *args, **kwargs):
        """
        Run the command by:
            - Finding all the Self Managed Members with Users who are about to expire
            - Iterating through these Members, getting all said Users and emailing them
        """
        self.range_start = datetime.now().date() + timedelta(days=4)
        self.range_end = datetime.now().date() + timedelta(days=32)

        emails: Deque[EmailMultiAlternatives] = deque()
        emails.extend(self.get_self_managed_emails())
        emails.extend(self.get_non_self_managed_emails())

        self.stdout.write('Sending emails.')
        self.send_emails(emails)

    def get_self_managed_emails(self):
        """
        Create the emails that need to be sent to admins in self-managed members
        :returns: A deque of email objects
        """
        # Get the members that need to be notified
        self_managed_member_ids = User.objects.filter(
            expiry_date__range=(self.range_start, self.range_end),
            administrator=False,
            member__self_managed=True,
            member__deleted__isnull=True,
        ).distinct().values_list(
            'member_id',
            flat=True,
        )

        members = Member.objects.filter(
            id__in=self_managed_member_ids,
        ).prefetch_related(
            Prefetch(
                'user_set',
                User.objects.filter(administrator=True).order_by('surname'),
                to_attr='admins',
            ),
            Prefetch(
                'user_set',
                User.objects.filter(
                    administrator=False,
                    expiry_date__range=(self.range_start, self.range_end),
                ).order_by(
                    'surname',
                ),
                to_attr='expiring_users',
            ),
        )

        # Create the Admin Emails
        emails: Deque[EmailMultiAlternatives] = deque()
        for member in members:
            for admin in member.admins:
                txt, html = [
                    render_to_string(
                        f'email/admin_expiry_reminder.{version}',
                        context={
                            'member': member,
                            'admin': admin,
                            'users': member.expiring_users,
                        },
                    ) for version in ['txt', 'html']
                ]
                emails.append(self.create_email(
                    user=admin,
                    subject=f'{settings.ORGANIZATION_URL} Membership User is about to expire!',
                    body_txt=txt,
                    body_html=html,
                ))

        return emails

    def get_non_self_managed_emails(self) -> Deque[EmailMultiAlternatives]:
        """
        Create the emails that need to be sent to the admins in charge of non-self-managed partner members
        :returns: A deque of email objects
        """
        # Get the users in non-self-managed Members who are expiring
        expiring_users = User.objects.filter(
            expiry_date__range=(self.range_start, self.range_end),
            administrator=False,
            member__self_managed=False,
            member__deleted__isnull=True,
        ).prefetch_related(
            # Prefetch the Link to the partner that created the non-self-managed Member
            Prefetch(
                'member__member',
                MemberLink.objects.exclude(contra_member_id=F('member_id')),
                'links',
            ),
        )

        # Get the Members that manage these users
        members_to_notify = {u.member.links[0].contra_member_id for u in expiring_users}
        members = Member.objects.filter(
            id__in=members_to_notify,
        ).order_by(
            'id',
        ).prefetch_related(
            Prefetch(
                'user_set',
                User.objects.filter(administrator=True),
                to_attr='admins',
            ),
        )

        # Cast these members to dictionaries to make it easier to link up with the expiring users
        partner_members = dict()
        for m in members:
            partner_members[m.id] = {
                'member': m,
                'admins': m.admins,
                'expiring_users': list(),
            }
        for u in expiring_users:
            partner_members[u.member.links[0].contra_member_id]['expiring_users'].append(u)

        emails: Deque[EmailMultiAlternatives] = deque()
        for item in partner_members.values():
            for admin in item['admins']:
                txt, html = [
                    render_to_string(
                        f'email/non_self_managed_expiry_email.{version}',
                        context={
                            'member': item['member'],
                            'admin': admin,
                            'users': item['expiring_users'],
                        },
                    ) for version in ['txt', 'html']
                ]

                emails.append(self.create_email(
                    user=admin,
                    subject=(
                        f'{settings.ORGANIZATION_URL} Membership Users in Non-Self-Managed Partners will soon expire'
                    ),
                    body_txt=txt,
                    body_html=html,
                ))
        return emails

    def create_email(self, user: User, subject: str, body_txt: str, body_html: str):
        """
        Create an email object with the given parameters
        :param user: The user who will receive the email
        :param subject: The subject of the email
        :param body_txt: The body of the email in plain text
        :param body_html: The body of the email in html
        :return:
        """
        if settings.PRODUCTION_DEPLOYMENT:
            to = [f'{user.first_name} {user.surname} <{user.email}>']
        else:
            to = settings.DEVELOPER_EMAILS

        email = EmailMultiAlternatives(
            from_email=settings.EMAIL_HOST_USER,
            to=to,
            subject=subject,
            body=body_txt,
        )
        email.attach_alternative(body_html, 'text/html')
        return email

    def send_emails(self, emails: Deque[EmailMultiAlternatives]):
        mail_backend = ExpirationBackend()
        successes = mail_backend.send_messages(emails, self.stdout)
        self.stdout.write(f'Sent {successes} of {len(emails)} emails successfully!')
