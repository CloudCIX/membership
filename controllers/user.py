# stdlib
import base64
import binascii
import logging
import random
import re
from collections import deque
from datetime import datetime
from io import BytesIO
from json import dumps
from minio.error import BucketAlreadyExists, BucketAlreadyOwnedByYou, ResponseError
from typing import cast, Deque, Dict, List, Optional, Union
from uuid import uuid4
# libs
from cloudcix_rest.controllers import ControllerBase
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from pytz import timezone as get_timezone, UnknownTimeZoneError
# local
from membership.utils import get_minio_client, MinioException
from membership.models import (
    Address,
    AddressLink,
    AppSettings,
    Language,
    Profile,
    Department,
    TransactionType,
    User,
)


__all__ = [
    'UserListController',
    'UserCreateController',
    'UserUpdateController',
]

BUCKET_NAME = 'user-images'
PHONE_PATTERN = re.compile(r'^(\(?\+?[0-9]*\)?)?[0-9_\- ()]*$')

logger = logging.getLogger(__name__)

Notification = Dict[str, Union[int, bool]]


class UserListController(ControllerBase):
    """
    Validates user data used to filter a list of User records
    """

    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this controller
        """

        allowed_ordering = (
            'id',
            'address__name',
            'administrator',
            'email',
            'expiry_date',
            'first_name',
            'last_login',
            'member__name',
            'start_date',
            'surname',
        )
        search_fields = {
            'address_id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'address__name': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'administrator': (),
            'department_id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'email': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'expiry_date': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'first_name': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'global_active': (),
            'global_user': (),
            'id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'job_title': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'language_id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'last_login': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'member_id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'member__name': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'member__api_key': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'profile_id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'robot': (),
            'start_date': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'surname': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
        }


class UserCreateController(ControllerBase):
    """
    Validates user data used to create a new User record
    """

    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = User
        validation_order = (
            'address_id',
            'first_name',
            'surname',
            'email',
            'password',
            'global_user',
            'global_active',
            'is_private',
            'timezone',
            'start_date',
            'expiry_date',
            'language_id',
            'profile_id',
            'department_id',
            'job_title',
            'notifications',
            'phones',
            'image',
            'signature',
            'otp',
        )

    def validate_address_id(self, address_id: Optional[int]) -> Optional[str]:
        """
        description: The id of the Address that the User belongs to
        type: integer
        """
        # Ensure the address id is valid
        try:
            address = Address.objects.get(pk=int(cast(int, address_id)))
        except (ValueError, TypeError):
            return 'membership_user_create_101'
        except Address.DoesNotExist:
            return 'membership_user_create_102'
        # Check that address is linked to the requesting user's address
        try:
            address.link = AddressLink.objects.get(
                address_id=self.request.user.address['id'],
                contra_address=address,
            )
        except AddressLink.DoesNotExist:
            # Check to make sure this is still allowed
            if (self.request.user.id != 1 and
                    (self.request.user.member['id'] != address.member_id or not self.request.user.is_global)):
                return 'membership_user_create_103'
            # Here it's okay for the link to be None
            address.link = None  # pragma: no cover
        address.linked = address.link is not None
        # Store the address and member
        self.cleaned_data['address'] = address
        self.cleaned_data['member'] = address.member
        return None

    def validate_first_name(self, first_name: Optional[str]) -> Optional[str]:
        """
        description: The first name of the User
        type: string
        """
        if first_name is None:
            first_name = ''
        first_name = str(first_name).strip()
        if len(first_name) == 0:
            return 'membership_user_create_104'
        if len(first_name) > self.get_field('first_name').max_length:
            return 'membership_user_create_105'
        self.cleaned_data['first_name'] = first_name
        return None

    def validate_surname(self, surname: Optional[str]) -> Optional[str]:
        """
        description: The surname of the User
        type: string
        """
        if surname is None:
            surname = ''
        surname = str(surname).strip()
        if len(surname) == 0:
            return 'membership_user_create_106'
        if len(surname) > self.get_field('surname').max_length:
            return 'membership_user_create_107'
        self.cleaned_data['surname'] = surname
        return None

    def validate_email(self, email: Optional[str]) -> Optional[str]:
        """
        description: |
            The email address of the User. Used to log in to CloudCIX. No other User in the Member can have the email.
        type: string
        """
        if 'member' not in self.cleaned_data:
            return None
        if email is None:
            email = ''
        email = str(email).strip()
        if len(email) == 0:
            return 'membership_user_create_108'
        if len(email) > self.get_field('email').max_length:
            return 'membership_user_create_109'
        # Ensure it is a valid email
        try:
            validate_email(email)
        except ValidationError:
            return 'membership_user_create_110'
        # Check to make sure that another User with the same email does not exist in the same Member
        if User.objects.filter(email=email, member=self.cleaned_data['member']).exists():
            return 'membership_user_create_111'
        # We don't want case sensitivity, so make it lowercase
        self.cleaned_data['email'] = email.lower()
        return None

    def validate_password(self, password: Optional[str]) -> Optional[str]:
        """
        description: The password for the User to log in with
        type: string
        """
        if not password:
            password = ''
        password = str(password).strip()
        if len(password) == 0:
            return 'membership_user_create_112'
        self.cleaned_data['password'] = password
        return None

    def validate_global_user(self, global_user: Optional[bool]) -> Optional[str]:
        """
        description: A flag stating whether the User can act as a global User
        type: boolean
        required: false
        """
        if global_user is None:
            global_user = False
        if not isinstance(global_user, bool):
            return 'membership_user_create_113'
        self.cleaned_data['global_user'] = global_user
        return None

    def validate_global_active(self, global_active: Optional[bool]) -> Optional[str]:
        """
        description: A flag stating whether the User should currently be a global User
        type: boolean
        required: false
        """
        if global_active is None:
            global_active = False
        if not isinstance(global_active, bool):
            return 'membership_user_create_114'
        self.cleaned_data['global_active'] = global_active and self.cleaned_data['global_user']
        return None

    def validate_is_private(self, is_private: Optional[bool]) -> Optional[str]:
        """
        description: A flag stating whether the User can act as a is_private User
        type: boolean
        required: false
        """
        if is_private is None:
            is_private = False
        if not isinstance(is_private, bool):
            return 'membership_user_create_115'
        self.cleaned_data['is_private'] = is_private
        return None

    def validate_timezone(self, timezone: Optional[str]) -> Optional[str]:
        """
        description: The timezone that the User is living in
        type: string
        """
        try:
            get_timezone(str(timezone))
        except (UnknownTimeZoneError, AttributeError):
            return 'membership_user_create_116'
        self.cleaned_data['timezone'] = timezone
        return None

    def validate_start_date(self, start_date: Optional[str]) -> Optional[str]:
        """
        description: The date on which the User started working for the company
        type: string
        """
        try:
            self.cleaned_data['start_date'] = datetime.strptime(str(start_date).split('T')[0], '%Y-%m-%d')
        except (TypeError, ValueError):
            return 'membership_user_create_117'
        return None

    def validate_expiry_date(self, expiry: Optional[str]) -> Optional[str]:
        """
        description: The date on which the User's account should expire, if they are not an administrator
        type: string
        """
        if 'start_date' not in self.cleaned_data:
            return None
        try:
            expiry_date = datetime.strptime(str(expiry).split('T')[0], '%Y-%m-%d')
        except (TypeError, ValueError):
            return 'membership_user_create_118'
        # Check that it's valid compared to the start date
        if expiry_date <= self.cleaned_data['start_date']:
            return 'membership_user_create_119'
        if expiry_date < datetime.utcnow():
            return 'membership_user_create_120'
        self.cleaned_data['expiry_date'] = expiry_date
        return None

    def validate_language_id(self, language_id: Optional[int]) -> Optional[str]:
        """
        description: The id of the Language used by the User
        type: integer
        """
        try:
            self.cleaned_data['language'] = Language.objects.get(pk=int(cast(int, language_id)))
        except (TypeError, ValueError):
            return 'membership_user_create_121'
        except Language.DoesNotExist:
            return 'membership_user_create_122'
        return None

    def validate_profile_id(self, profile_id: Optional[int]) -> Optional[str]:
        """
        description: The id of the Profile that the User should belong to
        type: integer
        required: false
        """
        if profile_id is None or 'member' not in self.cleaned_data:
            self.cleaned_data['profile'] = None
            return None
        try:
            self.cleaned_data['profile'] = Profile.objects.get(
                pk=int(profile_id),
                member=self.cleaned_data['member'],
            )
        except ValueError:
            return 'membership_user_create_123'
        except Profile.DoesNotExist:
            return 'membership_user_create_124'
        return None

    def validate_department_id(self, department_id: Optional[int]) -> Optional[str]:
        """
        description: The id of the Department that the User should belong to
        type: integer
        required: false
        """
        if department_id is None or 'member' not in self.cleaned_data:
            self.cleaned_data['department'] = None
            return None
        try:
            self.cleaned_data['department'] = Department.objects.get(
                pk=int(department_id),
                member=self.cleaned_data['member'],
            )
        except ValueError:
            return 'membership_user_create_125'
        except Department.DoesNotExist:
            return 'membership_user_create_126'
        return None

    def validate_job_title(self, job_title: Optional[str]) -> Optional[str]:
        """
        description: The User's job title
        type: string
        required: false
        """
        if job_title is None:
            job_title = ''
        job_title = str(job_title).strip()
        if len(job_title) > self.get_field('job_title').max_length:
            return 'membership_user_create_127'
        self.cleaned_data['job_title'] = job_title
        return None

    def validate_otp(self, otp: Optional[bool]) -> Optional[str]:
        """
        description: A flag stating whether the User will have Two Factor Authentication (2FA)
        type: boolean
        required: false
        """
        if otp is None:
            otp = False
        if not isinstance(otp, bool):
            return 'membership_user_create_138'
        self.cleaned_data['otp'] = otp
        if 'member' not in self.cleaned_data:
            return None
        if (not self.request.user.administrator
                and self.request.user.member['id'] != self.cleaned_data['member'].id):
            return None
        if otp is True:
            self.cleaned_data['first_otp'] = random.randint(100000, 1000000)
        return None

    @staticmethod
    def validate_notifications(notifications: Optional[List[Notification]]) -> Optional[str]:
        """
        description: |
            An array of details to set up Notifications for the User.

            Notifications can be set up for "internal" and "external" Transactions. A User set up to receive "internal"
            Notifications will be notified when another User in their Member creates a Transaction of that type, whereas
            a User set up to receive "external" Notifications will be notified when someone in a different Member
            creates a Transaction of that type that is sent to the User's Member.
        type: array
        items:
            type: object
            properties:
                transaction_type_id:
                    description: The id of the Transaction Type this User should receive Notifications for
                    type: integer
                external:
                    description: |
                        A flag stating whether the Notification should be for external (true) or internal (false)
                        Transactions.
                    default: true
            required:
                - transaction_type_id
        required: false
        """
        if notifications is None:
            return None
        ids: Deque[int] = deque()
        try:
            for transaction_type in notifications:
                t_id = int(transaction_type['transaction_type_id'])
                if t_id <= 0:
                    raise ValueError
                ids.append(t_id)
        except (TypeError, ValueError, KeyError):
            return 'membership_user_create_128'
        transaction_types = TransactionType.objects.filter(pk__in=ids).count()
        if len(ids) != transaction_types:
            return 'membership_user_create_129'
        return None

    def validate_phones(self, phones: Optional[List[Dict[str, str]]]) -> Optional[str]:
        """
        description: An array of named phone numbers that can be used to contact the User
        type: array
        items:
            type: object
            properties:
                name:
                    type: string
                number:
                    type: string
        required: false
        """
        phones = phones or []
        if not isinstance(phones, list):
            return 'membership_user_create_130'
        numbers: Deque = deque()
        for i, phone in enumerate(phones):
            if not isinstance(phone, dict):
                return 'membership_user_create_131'
            name = phone.get('name', None)
            number = phone.get('number', None)
            if name is None or number is None:
                return 'membership_user_create_132'
            if not PHONE_PATTERN.match(number):
                return 'membership_user_create_133'
            key = {'name': name.strip(), 'number': number.strip()}
            if key not in numbers:
                numbers.append(key)
        self.cleaned_data['phones'] = list(numbers)
        return None

    def validate_image(self, image: Optional[Union[Dict[str, str], str]]):
        """
        description: The data of an image to use for the User's profile picture. Alternatively, send a URL in a string.
        type: object
        properties:
            name:
                description: name of the image file
                type: string
            data:
                description: The image encoded in base64
                type: string
        required: false
        """
        if image is None:
            # Unset the image
            self.cleaned_data['image'] = None
            return
        if isinstance(image, dict):
            try:
                filename: str = f'{uuid4()}.{image["name"].split(".")[1]}'
                data: bytes = base64.b64decode(image['data'])
                filesize: int = len(data)
            except KeyError:
                return 'membership_user_create_134'
            except binascii.Error:
                return 'membership_user_create_135'

            # Check that our variables are valid
            if filesize == 0:
                return 'membership_user_create_136'
            try:
                minio = get_minio_client()
            except MinioException:
                logger.error('Settings for MinIO are not configured', exc_info=True)
                # MinIO not configured, won't fail entire request but am logging reason
                return
            # Create the container if it doesn't already exist
            try:
                minio.make_bucket(BUCKET_NAME)
            except (BucketAlreadyExists, BucketAlreadyOwnedByYou):
                # These are fine
                pass
            except ResponseError:  # pragma: no cover
                # This is bad, log error and return
                logger.error('Failed to connect to Minio', exc_info=True)
                # Don't fail the entire request just log the error
                return
            else:  # pragma: no cover
                # Make the bucket readable publicly
                policy = {
                    'Version': '2012-10-17',
                    'Statement': [{
                        'Sid': 'AddPerm',
                        'Effect': 'Allow',
                        'Principal': '*',
                        'Action': ['s3:GetObject'],
                        'Resource': [f'arn:aws:s3:::{BUCKET_NAME}/*'],
                    }],
                }
                minio.set_bucket_policy(BUCKET_NAME, dumps(policy))

            # Now try uploading the file
            try:
                minio.put_object(BUCKET_NAME, filename, BytesIO(data), filesize)
            except ResponseError:  # pragma: no cover
                # This is bad, log error and return
                logger.error('Failed to upload file to Minio', exc_info=True)
                # Don't fail the entire request just log the error
                return
            app_settings = AppSettings.objects.filter()[0]
            image = f'https://{app_settings.minio_url.rstrip("/")}/{BUCKET_NAME}/{filename}'
        elif not isinstance(image, str):
            return 'membership_user_create_137'
        self.cleaned_data['image'] = image
        return None

    def validate_signature(self, signature: Optional[str]) -> Optional[str]:
        """
        description: The User's email signature
        type: string
        required: false
        """
        self.cleaned_data['signature'] = str(signature).strip() if signature is not None else ''
        return None


class UserUpdateController(ControllerBase):
    """
    Validates user data used to update a User record
    """

    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = User
        validation_order = (
            'address_id',
            'first_name',
            'surname',
            'email',
            'password',
            'global_user',
            'global_active',
            'is_private',
            'timezone',
            'start_date',
            'expiry_date',
            'language_id',
            'profile_id',
            'department_id',
            'job_title',
            'notifications',
            'phones',
            'image',
            'signature',
            'login',
            'otp',
            'first_otp',
            'administrator',
            'robot',
        )

    def validate_address_id(self, address_id: Optional[int]) -> Optional[str]:
        """
        description: |
            The id of the Address that the User belongs to. Only a global user can update this, and it must be to
            another Address in the Member.
        type: integer
        """
        # Ensure the address id is valid
        try:
            address = Address.objects.get(pk=int(cast(int, address_id)))
        except (ValueError, TypeError):
            return 'membership_user_update_101'
        except Address.DoesNotExist:
            return 'membership_user_update_102'
        # Check that address is linked to the requesting user's address
        try:
            address.link = AddressLink.objects.get(
                address_id=self.request.user.address['id'],
                contra_address=address,
            )
        except AddressLink.DoesNotExist:
            # Check to make sure this is still allowed
            if (self.request.user.id != 1 and
                    (self.request.user.member['id'] != address.member_id or not self.request.user.is_global)):
                return 'membership_user_update_103'
            # Here it's okay for the link to be None
            address.link = None
        address.linked = address.link is not None
        # Check that the user is not changing the member of the address
        if self._instance.member_id != address.member_id:
            return 'membership_user_update_104'
        # Store the address
        self.cleaned_data['address'] = address
        return None

    def validate_first_name(self, first_name: Optional[str]) -> Optional[str]:
        """
        description: The first name of the User
        type: string
        """
        if first_name is None:
            first_name = ''
        first_name = str(first_name).strip()
        if len(first_name) == 0:
            return 'membership_user_update_105'
        if len(first_name) > self.get_field('first_name').max_length:
            return 'membership_user_update_106'
        self.cleaned_data['first_name'] = first_name
        return None

    def validate_surname(self, surname: Optional[str]) -> Optional[str]:
        """
        description: The surname of the User
        type: string
        """
        if surname is None:
            surname = ''
        surname = str(surname).strip()
        if len(surname) == 0:
            return 'membership_user_update_107'
        if len(surname) > self.get_field('surname').max_length:
            return 'membership_user_update_108'
        self.cleaned_data['surname'] = surname
        return None

    def validate_email(self, email: Optional[str]) -> Optional[str]:
        """
        description: |
            The email address of the User. Used to log in to CloudCIX. No other User in the Member can have the email.
            Only an admin can update this.
        type: string
        """
        if not self.request.user.administrator:
            self.cleaned_data['email'] = self._instance.email
            return None
        address = self.cleaned_data.get('address', self._instance.address)
        if email is None:
            email = ''
        email = str(email).strip()
        if len(email) == 0:
            return 'membership_user_update_109'
        if len(email) > self.get_field('email').max_length:
            return 'membership_user_update_110'
        # Ensure it is a valid email
        try:
            validate_email(email)
        except ValidationError:
            return 'membership_user_update_111'
        # Check to make sure that another User with the same email does not exist in the same Address
        if User.objects.filter(
            email=email,
            member=address.member,
        ).exclude(
            pk=self._instance.pk,
        ).exists():
            return 'membership_user_update_112'
        # We don't want case sensitivity, so make it lowercase
        self.cleaned_data['email'] = email.lower()
        return None

    def validate_password(self, password: Optional[str]) -> Optional[str]:
        """
        description: The password for the User to log in with
        type: string
        """
        if not password:
            password = ''
        password = str(password).strip()
        if len(password) == 0:
            # It's okay to not sent a password here
            self.cleaned_data['password'] = None
            return None
        self.cleaned_data['password'] = password
        return None

    def validate_global_user(self, global_user: Optional[bool]) -> Optional[str]:
        """
        description: A flag stating whether the User can act as a global User. Only an admin can update this.
        type: boolean
        required: false
        """
        if not self.request.user.administrator or global_user is None:
            global_user = self._instance.global_user
        if not isinstance(global_user, bool):
            return 'membership_user_update_113'
        self.cleaned_data['global_user'] = global_user
        return None

    def validate_global_active(self, global_active: Optional[bool]) -> Optional[str]:
        """
        description: A flag stating whether the User should currently be a global User. Only an admin can update this.
        type: boolean
        required: false
        """
        if not self.request.user.administrator or global_active is None:
            global_active = self._instance.global_active
        if not isinstance(global_active, bool):
            return 'membership_user_update_114'
        self.cleaned_data['global_active'] = (
            global_active and self.cleaned_data.get('global_user', self._instance.global_user)
        )
        return None

    def validate_is_private(self, is_private: Optional[bool]) -> Optional[str]:
        """
        description: A flag stating whether the User can act as a is_private User.
        type: boolean
        required: false
        """
        if is_private is None:
            is_private = self._instance.is_private
        if not isinstance(is_private, bool):
            return 'membership_user_update_115'
        self.cleaned_data['is_private'] = is_private
        return None

    def validate_timezone(self, timezone: Optional[str]) -> Optional[str]:
        """
        description: The timezone that the User is living in
        type: string
        """
        try:
            get_timezone(str(timezone))
        except (UnknownTimeZoneError, AttributeError):
            return 'membership_user_update_116'
        self.cleaned_data['timezone'] = timezone
        return None

    def validate_start_date(self, start_date: Optional[str]) -> Optional[str]:
        """
        description: The date on which the User started working for the company. Only an admin can update this.
        type: string
        """
        if not self.request.user.administrator:
            self.cleaned_data['start_date'] = self._instance.start_date
            return None
        try:
            self.cleaned_data['start_date'] = datetime.strptime(str(start_date).split('T')[0], '%Y-%m-%d')
        except (TypeError, ValueError):
            return 'membership_user_update_117'
        return None

    def validate_expiry_date(self, expiry: Optional[str]) -> Optional[str]:
        """
        description: |
            The date on which the User's account should expire, if they are not an administrator.
            Only an admin can update this.
        type: string
        """
        if not self.request.user.administrator:
            self.cleaned_data['expiry_date'] = self._instance.expiry_date
            return None
        try:
            expiry_date = datetime.strptime(str(expiry).split('T')[0], '%Y-%m-%d')
        except (TypeError, ValueError):
            return 'membership_user_update_118'
        # Check that it's valid compared to the start date
        if 'start_date' in self.cleaned_data:
            if expiry_date <= self.cleaned_data['start_date']:
                return 'membership_user_update_119'
        elif expiry_date <= self._instance.start_date:
            return 'membership_user_update_120'
        self.cleaned_data['expiry_date'] = expiry_date
        return None

    def validate_language_id(self, language_id: Optional[int]) -> Optional[str]:
        """
        description: The id of the Language used by the User
        type: integer
        """
        try:
            self.cleaned_data['language'] = Language.objects.get(pk=int(cast(int, language_id)))
        except (TypeError, ValueError):
            return 'membership_user_update_121'
        except Language.DoesNotExist:
            return 'membership_user_update_122'
        return None

    def validate_profile_id(self, profile_id: Optional[int]) -> Optional[str]:
        """
        description: |
            The id of the Profile that the User should belong to.
            Only an administrator can update this field.
        type: integer
        required: false
        """
        if not self.request.user.administrator:
            self.cleaned_data['profile'] = self._instance.profile
            return None
        if profile_id is None:
            self.cleaned_data['profile'] = None
            return None
        try:
            self.cleaned_data['profile'] = Profile.objects.get(pk=int(profile_id), member=self._instance.member)
        except ValueError:
            return 'membership_user_update_123'
        except Profile.DoesNotExist:
            return 'membership_user_update_124'
        return None

    def validate_department_id(self, department_id: Optional[int]) -> Optional[str]:
        """
        description: |
            The id of the Department that the User should belong to.
            Only an administrator can update this field.
        type: integer
        required: false
        """
        if not self.request.user.administrator:
            self.cleaned_data['department'] = self._instance.department
            return None
        if department_id is None:
            self.cleaned_data['department'] = None
            return None
        try:
            self.cleaned_data['department'] = Department.objects.get(
                pk=int(department_id),
                member=self._instance.member,
            )
        except ValueError:
            return 'membership_user_update_125'
        except Department.DoesNotExist:
            return 'membership_user_update_126'
        return None

    def validate_job_title(self, job_title: Optional[str]) -> Optional[str]:
        """
        description: The User's job title. Only an admin can update this field.
        type: string
        required: false
        """
        if not self.request.user.administrator:
            self.cleaned_data['job_title'] = self._instance.job_title
            return None
        if job_title is None:
            job_title = ''
        job_title = str(job_title).strip()
        if len(job_title) > self.get_field('job_title').max_length:
            return 'membership_user_update_127'
        self.cleaned_data['job_title'] = job_title
        return None

    @staticmethod
    def validate_notifications(notifications: Optional[List[Notification]]) -> Optional[str]:
        """
        description: |
            An array of details to set up Notifications for the User.

            Notifications can be set up for "internal" and "external" Transactions. A User set up to receive "internal"
            Notifications will be notified when another User in their Member creates a Transaction of that type, whereas
            a User set up to receive "external" Notifications will be notified when someone in a different Member
            creates a Transaction of that type that is sent to the User's Member.
        type: array
        items:
            type: object
            properties:
                transaction_type_id:
                    description: The id of the Transaction Type this User should receive Notifications for
                    type: integer
                external:
                    description: |
                        A flag stating whether the Notification should be for external (true) or internal (false)
                        Transactions.
                    default: true
            required:
                - transaction_type_id
        required: false
        """
        if notifications is None:
            return None
        ids: Deque[int] = deque()
        try:
            for transaction_type in notifications:
                t_id = int(transaction_type['transaction_type_id'])
                if t_id <= 0:
                    raise ValueError
                ids.append(t_id)
        except (TypeError, ValueError, KeyError):
            return 'membership_user_update_128'
        transaction_types = TransactionType.objects.filter(pk__in=ids).count()
        if len(ids) != transaction_types:
            return 'membership_user_update_129'
        return None

    def validate_phones(self, phones: Optional[List[Dict[str, str]]]) -> Optional[str]:
        """
        description: An array of named phone numbers that can be used to contact the User
        type: array
        items:
            type: object
            properties:
                name:
                    type: string
                number:
                    type: string
        required: false
        """
        phones = phones or []
        if not isinstance(phones, list):
            return 'membership_user_update_130'
        numbers: Deque = deque()
        for i, phone in enumerate(phones):
            if not isinstance(phone, dict):
                return 'membership_user_update_131'
            name = phone.get('name', None)
            number = phone.get('number', None)
            if name is None or number is None:
                return 'membership_user_update_132'
            if not PHONE_PATTERN.match(number):
                return 'membership_user_update_133'
            key = {'name': name.strip(), 'number': number.strip()}
            if key not in numbers:
                numbers.append(key)
        self.cleaned_data['phones'] = list(numbers)
        return None

    def validate_image(self, image: Optional[Union[Dict[str, str], str]]):
        """
        description: The data of an image to use for the User's profile picture. Alternatively, send a URL in a string.
        type: object
        properties:
            name:
                description: name of the image file
                type: string
            data:
                description: The image encoded in base64
                type: string
        required: false
        """
        if image is None:
            # Unset the image
            self._delete_old_image(self._instance.image)
            self.cleaned_data['image'] = None
            return
        if isinstance(image, dict):
            try:
                filename: str = f'{uuid4()}.{image["name"].split(".")[1]}'
                data: bytes = base64.b64decode(image['data'])
                filesize: int = len(data)
            except KeyError:
                return 'membership_user_update_134'
            except binascii.Error:
                return 'membership_user_update_135'

            # Check that our variables are valid
            if filesize == 0:
                return 'membership_user_update_136'

            try:
                minio = get_minio_client()
            except MinioException:
                logger.error('Settings for MinIO are not configured', exc_info=True)
                # MinIO not configured, won't fail entire request but am logging reason
                return
            # Create the container if it doesn't already exist
            try:
                minio.make_bucket(BUCKET_NAME)
            except (BucketAlreadyExists, BucketAlreadyOwnedByYou):
                # These are fine
                pass
            except ResponseError:  # pragma: no cover
                # This is bad, log error and return
                logger.error('Failed to connect to Minio', exc_info=True)
                # Don't fail the entire request just log the error
                return
            else:  # pragma: no cover
                # Make the bucket readable publicly
                policy = {
                    'Version': '2012-10-17',
                    'Statement': [{
                        'Sid': 'AddPerm',
                        'Effect': 'Allow',
                        'Principal': '*',
                        'Action': ['s3:GetObject'],
                        'Resource': [f'arn:aws:s3:::{BUCKET_NAME}/*'],
                    }],
                }
                minio.set_bucket_policy(BUCKET_NAME, dumps(policy))

            # Now try uploading the file
            try:
                minio.put_object(BUCKET_NAME, filename, BytesIO(data), filesize)
            except ResponseError:  # pragma: no cover
                # This is bad, log error and return
                logger.error('Failed to upload file to Minio', exc_info=True)
                # Don't fail the entire request just log the error
                return
            app_settings = AppSettings.objects.filter()[0]
            image = f'https://{app_settings.minio_url.rstrip("/")}/{BUCKET_NAME}/{filename}'
        elif not isinstance(image, str):
            return 'membership_user_update_137'
        # Delete old image
        if image != self._instance.image:
            self._delete_old_image(self._instance.image)
        self.cleaned_data['image'] = image
        return None

    def validate_signature(self, signature: Optional[str]) -> Optional[str]:
        """
        description: The User's email signature
        type: string
        required: false
        """
        self.cleaned_data['signature'] = str(signature).strip() if signature is not None else ''
        return None

    def validate_login(self, login: Optional[bool]):  # pragma: no cover
        """
        description: |
            Update the User's last login date and time to the current date and time.
            Only usable by certain Users, ignored for all others.
        type: boolean
        required: false
        """
        if login is None:
            login = False
        if self.request.user.is_super and isinstance(login, bool) and login:
            self.cleaned_data['last_login'] = datetime.utcnow()

    def _delete_old_image(self, image: Optional[str]):  # pragma: no cover
        """
        Delete the old image that the user has, if they had any originally
        """
        if image is None:
            return
        try:
            minio = get_minio_client()
        except MinioException:
            logger.error('Settings for MinIO are not configured', exc_info=True)
            # MinIO not configured, won't fail entire request but am logging reason
            return
        # The image is a url with the filename being at the end
        filename = image.split('/')[-1]
        try:
            minio.remove_object(BUCKET_NAME, filename)
        except ResponseError:
            logger.error('Failed to delete old image from Minio', exc_info=True)

    def validate_otp(self, otp: Optional[bool]) -> Optional[str]:
        """
        description: A flag stating whether the User will have Two Factor Authentication (2FA)
        type: boolean
        """
        if ((not self.request.user.administrator and
                self.request.user.member['id'] != self._instance.member_id) or otp is None):
            self.cleaned_data['otp'] = self._instance.otp
            return None
        if not isinstance(otp, bool):
            return 'membership_user_update_138'
        self.cleaned_data['otp'] = otp
        return None

    def validate_first_otp(self, first_otp: Optional[int]) -> Optional[str]:
        """
        description: |
            A number that will be used in the Two Factor Authentication (2fa) creation.
            Must be a six digit number between 100000 and 999999 inclusive.
        type: string
        required: false
        """

        if (not self.request.user.administrator and
                self.request.user.member['id'] != self._instance.member_id):
            self.cleaned_data['first_otp'] = self._instance.first_otp
            return None
        if first_otp is None:
            self.cleaned_data['first_otp'] = first_otp
            return None
        if not isinstance(first_otp, int):
            return 'membership_user_update_139'
        otp = self.cleaned_data['otp']
        if otp is True:
            if first_otp not in range(100000, 1000000):
                return 'membership_user_update_140'
        else:
            return 'membership_user_update_141'
        self.cleaned_data['first_otp'] = first_otp
        return None

    def validate_administrator(self, administrator: Optional[bool]) -> Optional[str]:
        """
        description: A flag stating if User is an Administrator
        type: boolean
        required: false
        """
        # administrator is optional
        if administrator is None:
            self.cleaned_data['administrator'] = self._instance.administrator
            return None

        # If it was sent, ensure it's a boolean
        if not isinstance(administrator, bool):
            return 'membership_user_update_142'

        self.cleaned_data['administrator'] = administrator
        return None

    def validate_robot(self, robot: Optional[bool]) -> Optional[str]:
        """
        description: |
            A flag stating if User is a Robot. Only one user in an Address which is a cloud_region can have this role.
        type: boolean
        required: false
        """
        # robot is optional
        if robot is None:
            self.cleaned_data['robot'] = self._instance.robot
            return None

        # If it was sent, ensure it's a boolean
        if not isinstance(robot, bool):
            return 'membership_user_update_143'

        address = self.cleaned_data.get('address', self._instance.address)

        # Make sure the Address is a region
        if robot and not address.cloud_region:
            return 'membership_user_update_144'

        # Ensure there is only one robot in the region
        if User.objects.filter(
            address=address,
            robot=True,
        ).exclude(
            pk=self._instance.pk,
        ).exists():
            return 'membership_user_update_145'

        self.cleaned_data['robot'] = robot
        return None

    def is_valid(self) -> bool:
        """
        Run any extra validation on cleaned fields
        """
        is_valid = super(UserUpdateController, self).is_valid()
        if not is_valid:
            return is_valid

        # Make sure OTP is not turned on for robots or an API user
        otp = self.cleaned_data.get('otp', self._instance.otp)
        if otp:
            is_api_user = self._instance.id == 1
            is_robot = self.cleaned_data.get('robot', self._instance.robot)
            if is_api_user or is_robot:
                self._errors['otp'] = 'membership_user_update_146'
                is_valid = False

        return is_valid
