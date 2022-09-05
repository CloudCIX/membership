# stdlib
import crypt
import hmac
import logging
from minio import Minio
# lib
import ldap3
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
# local
from membership.models import AppSettings


class MinioError(Exception):
    pass


__all__ = [
    'clear_user_cache',
    'get_minio_client',
    'ldap_add_memberuid',
    'ldap_auth',
    'ldap_create',
    'ldap_delete',
    'ldap_exists',
    'ldap_remove_memberuid',
    'ldap_update_password',
]


def clear_user_cache(user_id):

    cache_key = f'user_{user_id}'
    if cache.get(cache_key):  # pragma: no cover
        cache.delete(cache_key)

    return None


def get_minio_client() -> Minio:
    """
    Utility function to create a Minio client instance
    """
    try:
        app_settings = AppSettings.objects.filter()[0]
    except IndexError:
        raise MinioError

    if app_settings.minio_url is None or app_settings.minio_access_key is None or app_settings.minio_secret_key is None:
        raise MinioError

    return Minio(
        app_settings.minio_url,
        access_key=app_settings.minio_access_key,
        secret_key=app_settings.minio_secret_key,
        secure=True,
    )


def ldap_add_memberuid(email, member_id):
    """
    Update an existing LDAP account by adding another memberUid to it.
    """
    logger = logging.getLogger('membership.utils.ldap_add_memberuid')
    conn = settings.LDAP_CONN

    cn = f'cn={email},{settings.LDAP_DOMAIN_CONTROLLER}'
    changes = {'memberUid': (ldap3.MODIFY_ADD, [member_id])}
    success = conn.modify(cn, changes)

    if not success:  # pragma: no cover
        logger.error(
            f'Error occurred when updating {email} with MemberUID {member_id} in LDAP. '
            f'ERROR: {conn.last_error}',
        )

    return success


def ldap_auth(email, password):
    """
    Verify sent crenditals are valid
    """
    conn = settings.LDAP_CONN

    try:
        validate_email(email)
    except ValidationError:
        # An email address was not sent
        return False

    if not conn.search(
        search_base=settings.LDAP_DOMAIN_CONTROLLER,
        search_filter=f'(&(uid={email}))',
        attributes=['userPassword'],
    ):
        # Email not found
        return False

    crypted_password = conn.response[0]['attributes']['userPassword'][0]
    if type(crypted_password) == bytes:  # pragma: no cover
        # Uncovered because I'm not 100% sure when this happens but I've seen it happen so I know it does
        crypted_password = crypted_password.decode()
    if not hmac.compare_digest(crypted_password, crypt.crypt(password, crypted_password)):
        # Incorrect password sent
        return False

    return True


def ldap_create(email, member_id, password):
    """
    Create an LDAP account
    """
    logger = logging.getLogger('membership.utils.ldap_create')

    conn = settings.LDAP_CONN
    cn = f'cn={email},{settings.LDAP_DOMAIN_CONTROLLER}'

    object_classes = ['account', 'extensibleObject']
    crypt_password = crypt.crypt(password, crypt.mksalt(crypt.METHOD_SHA512))
    attrs = {
        'uid': email,
        'userPassword': crypt_password,
        'memberUid': [member_id],
    }
    success = conn.add(cn, object_classes, attrs)

    if not success:  # pragma: no cover
        logger.error(
            f'Error occurred when creating LDAP entry for {email} with MemberUID {member_id}. '
            f'ERROR: {conn.last_error}',
        )

    return success


def ldap_delete(email):
    """
    Delete an LDAP account
    """
    logger = logging.getLogger('membership.utils.ldap_create')
    conn = settings.LDAP_CONN
    cn = f'cn={email},{settings.LDAP_DOMAIN_CONTROLLER}'

    success = conn.delete(cn)

    if not success:  # pragma: no cover
        logger.error(f'Error occurred when deleting LDAP entry for {email}. ERROR: {conn.last_error}')

    return success


def ldap_exists(email):
    """
    Check if an account for email exists in LDAP
    """
    conn = settings.LDAP_CONN

    exists = conn.search(
        search_base=settings.LDAP_DOMAIN_CONTROLLER,
        search_filter=f'(&(uid={email}))',
    )

    return exists


def ldap_remove_memberuid(email, member_id):
    """
    Update an existing LDAP account by removing memberUid from it
    """
    logger = logging.getLogger('membership.utils.ldap_remove_memberuid')

    conn = settings.LDAP_CONN

    cn = f'cn={email},{settings.LDAP_DOMAIN_CONTROLLER}'
    remove_memberuid = {'memberUid': (ldap3.MODIFY_DELETE, [member_id])}
    success = conn.modify(cn, remove_memberuid)

    if not success:  # pragma: no cover
        logger.error(
            f'Error occurred when updating {email} to remove MemberUID {member_id} in LDAP. ERROR: {conn.last_error}',
        )

    return success


def ldap_update_password(email, password):
    """
    Update the password for an existing LDAP account.
    """
    logger = logging.getLogger('membership.utils.ldap_update_password')

    conn = settings.LDAP_CONN
    cn = f'cn={email},{settings.LDAP_DOMAIN_CONTROLLER}'

    crypt_password = crypt.crypt(password, crypt.mksalt(crypt.METHOD_SHA512))
    update_password = {'userPassword': (ldap3.MODIFY_REPLACE, [crypt_password])}
    success = conn.modify(cn, update_password)

    if not success:  # pragma: no cover
        logger.error(
            f'Error occurred when updating password for {email} in LDAP. ERROR: {conn.last_error}',
        )

    return success
