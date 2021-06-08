"""
Handling for User authentication and Token management
"""

# stdlib
import crypt
import datetime
import hmac
# libs
import jwt
from cloudcix.api.otp import OTP
from cloudcix_rest.exceptions import Http400
from cloudcix_rest.views import APIView
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.request import Request
# local
from membership.models import User


__all__ = [
    'AuthResource',
]
with open(settings.PRIVATE_KEY_FILE) as f:
    PRIVATE_KEY = f.read()
with open(settings.PUBLIC_KEY_FILE) as f:
    PUBLIC_KEY = f.read()


class LoginPermission(BasePermission):
    """
    Custom DRF Permission for this class
    """

    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        elif request.user.is_authenticated:
            return True
        return False


class AuthResource(APIView):
    """
    Handles the authenticating and token generation for new users
    """
    permission_classes = (LoginPermission,)

    def post(self, request: Request) -> Response:
        """
        summary: Validate a User's credentials and generate a token if a valid api_key is sent.

        description: |
            If the user just sends an email and password, this service will attempt to authenticate them, returning a
            200 if the details are valid, and a 400 otherwise.

            If the user also sends an api_key, after validating the email and password, this service will attempt to
            create a token for the User with the specified email in the Member with the specified API key.
            This will return either a 201 if successful, or a 400 otherwise.

        responses:
            # 401 will always be added
            200:
                description: Sent email and password are valid
                # Putting content: none will overwrite the default and have no content
                content: none
            201:
                description: A token was successfully created
                # This view doesn't follow the Resource pattern
                content:
                    application/json:
                        schema:
                            $ref: '#/components/schemas/Auth'
            # Putting {} here means it will be completely populated with the defaults
            400: {}

        # Disable security on this method
        security: []
        """
        # Check that the necessary information is provided
        tracer = settings.TRACER
        conn = settings.LDAP_CONN
        data = request.data

        with tracer.start_span('checking_for_required_fields', child_of=request.span):
            if 'email' not in data or 'password' not in data:
                return Http400(error_code='membership_token_create_001')

        with tracer.start_span('searching_for_user', child_of=request.span):
            success = conn.search(
                search_base=settings.LDAP_DOMAIN_CONTROLLER,
                search_filter=f'(&(uid={data["email"]}))',
                attributes=['userPassword'],
            )
            if not success:
                return Http400(error_code='membership_token_create_002')

        # Check the user's crypted password against the sent password
        with tracer.start_span('checking_user_password', child_of=request.span):
            crypted_password = conn.response[0]['attributes']['userPassword'][0]
            if type(crypted_password) == bytes:  # pragma: no cover
                # Uncovered because I'm not 100% sure when this happens but I've seen it happen so I know it does
                crypted_password = crypted_password.decode()
            if not hmac.compare_digest(crypted_password, crypt.crypt(data['password'], crypted_password)):
                return Http400(error_code='membership_token_create_002')

        # At this point we know that the supplied details are valid.
        if 'api_key' not in data:
            # Return 200 to let the user know the auth is valid
            return Response({})

        # At this point, check if a user with that email exists in the supplied Member
        with tracer.start_span('ensure_valid_api_key', child_of=request.span):
            try:
                user = User.objects.values(
                    'pk',
                    'otp',
                    'first_otp',
                ).get(
                    email__iexact=data['email'],
                    member__api_key=data['api_key'],
                )

            except User.DoesNotExist:
                # If the User doesn't exist in the Member, return a 400
                return Http400(error_code='membership_token_create_003')

        # check if a user has otp, if they dont return an error which will then use the form
        with tracer.start_span('checking_otp', child_of=request.span):
            if user['otp'] and user['first_otp'] is not None:
                if 'first_otp' not in data:
                    return Http400(error_code='membership_token_create_004')
                else:
                    if data['first_otp'] is None:
                        return Http400(error_code='membership_token_create_005')
                    else:
                        if data['first_otp'] != user['first_otp']:
                            return Http400(error_code='membership_token_create_005')
                        else:
                            # get user and update first otp of user to none
                            u = User.objects.get(email__iexact=data['email'], member__api_key=data['api_key'])
                            u.first_otp = None
                            u.save()
            elif user['otp'] and user['first_otp'] is None:
                # User needs to send the six pin otp here.
                if 'otp' not in data:
                    return Http400(error_code='membership_token_create_006')
                else:
                    if data['otp'] is None:
                        return Http400(error_code='membership_token_create_007')
                    else:
                        request_data = {
                            'otp': data['otp'],
                        }
                        response = OTP.otp_auth.create(
                            data=request_data,
                            email=data['email'],
                        )
                        if response.status_code != 200:
                            return Http400(error_code='membership_token_create_007')
        # Create a token and return it in the response
        # Token will contain the user id since there is a specific id for each user / member mapping
        with tracer.start_span('create_token', child_of=request.span):
            payload = {
                'uid': user['pk'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=settings.TOKEN_VALID_HOURS),
            }
            token = jwt.encode(payload, PRIVATE_KEY, algorithm='RS256')

        return Response({'token': token}, status=status.HTTP_201_CREATED)

    def put(self, request: Request) -> Response:
        """
        summary: Create a new token for a user, given a valid request token.

        description: |
            Sending a request to this endpoint with a valid API token will generate a new token for the same User that
            will be valid for an hour.

            Use this method to refresh tokens without having to make the user log in multiple times.

        responses:
            200:
                description: New token for the User
                # This view doesn't follow the Resource pattern
                content:
                    application/json:
                        schema:
                            $ref: '#/components/schemas/Auth'
        """
        # Try to decrypt the payload, get the uid from it and build a new token if successful
        tracer = settings.TRACER

        with tracer.start_span('decode_token', child_of=request.span):
            try:
                uid = jwt.decode(request.auth, PUBLIC_KEY, algorithms=['RS256'])['uid']
            except jwt.PyJWTError:  # pragma: no cover
                # No cover because we should never get here anyway
                return Http400(error_code='membership_token_update_001')

        with tracer.start_span('create_new_token', child_of=request.span):
            payload = {
                'uid': uid,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            }
            token = jwt.encode(payload, PRIVATE_KEY, algorithm='RS256')

        return Response({'token': token})
