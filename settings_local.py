# Local settings that change on a per application / per environment basis
import atexit
import os
import ldap3

PGSQLAPI_PASSWORD = os.getenv('PGSQL_PASSWORD', 'pw')
PGSQLAPI_USER = os.getenv('PGSQL_USER', 'postgres')
PGSQLAPI_HOST = os.getenv('PGSQLAPI_HOST', 'pgsqlapi')
POD_NAME = os.getenv('POD_NAME', 'pod')
ORGANIZATION_URL = os.getenv('ORGANIZATION_URL', 'example.com')
LDAP_DOMAIN_CONTROLLER = os.getenv('MEMBERSHIPLDAP_DC', 'dc=example,dc=com')
LDAP_PASSWORD = os.getenv('MEMBERSHIPLDAP_PASSWORD', 'pw')
LDAP_URL = os.getenv('MEMBERSHIPLDAP_URL', 'membershipldap')
PAM_NAME = os.getenv('PAM_NAME', 'pam')
PAM_ORGANIZATION_URL = os.getenv('PAM_ORGANIZATION_URL', 'example.com')
PORTAL_NAME = os.getenv('PORTAL_NAME', 'saas')

ALLOWED_HOSTS = (
    f'membership.{POD_NAME}.{ORGANIZATION_URL}',
)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    'membership': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'membership',
        'USER': PGSQLAPI_USER,
        'PASSWORD': PGSQLAPI_PASSWORD,
        'HOST': PGSQLAPI_HOST,
        'PORT': '5432',
    },
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'django_default',
        'USER': PGSQLAPI_USER,
        'PASSWORD': PGSQLAPI_PASSWORD,
        'HOST': PGSQLAPI_HOST,
        'PORT': '5432',
    },
}

DATABASE_ROUTERS = [
    'membership.db_router.MembershipRouter',
]

# Increased post body size limit
# https://docs.djangoproject.com/en/2.0/ref/settings/#data-upload-max-memory-size
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880

DEBUG = False

EMAIL_CONFIRMATION_URL = f'https://{PORTAL_NAME}.{ORGANIZATION_URL}/auth/email-confirmation/'

INSTALLED_APPS = [
    'membership',
]

# Used as the search base in LDAP queries
# LDAP domain connection

LDAP_CONN = ldap3.Connection(
    ldap3.ServerPool([ldap3.Server(f'{LDAP_URL}:389') for _ in range(5)], active=True, exhaust=False),
    user=f'cn=admin,{LDAP_DOMAIN_CONTROLLER}',
    password=f'{LDAP_PASSWORD}',
    pool_size=2,
    pool_keepalive=10,
    pool_lifetime=60,
    client_strategy='RESTARTABLE',
)

LDAP_CONN.bind()
# Close the connection when the system closes
atexit.register(LDAP_CONN.unbind)

# Path to private key file for membership
PRIVATE_KEY_FILE = os.path.join(BASE_DIR, 'private-key.rsa')

# Small flag for whether or not this is a production deployment
PRODUCTION_DEPLOYMENT = os.getenv('PRODUCTION_DEPLOYMENT', 'true').lower() == 'true'
if not PRODUCTION_DEPLOYMENT:
    DEVELOPER_EMAILS = [os.getenv('DEVELOPER_EMAILS', 'developers@example.com')]

# Default is False
TESTING = os.getenv('TESTING', 'false').lower() == 'true'

TOKEN_VALID_HOURS = 2

USE_I18N = False
USE_L10N = False

ORG = ORGANIZATION_URL.split('.')[0]
APPLICATION_NAME = os.getenv('APPLICATION_NAME', f'{POD_NAME}_{ORG}_membership')


LOGSTASH_ENABLE = os.getenv('LOGSTASH_ENABLE', 'false').lower() == 'true'

if f'{PAM_NAME}.{PAM_ORGANIZATION_URL}' == 'support.cloudcix.com' or LOGSTASH_ENABLE:
    CLOUDCIX_INFLUX_TAGS = {
        'service_name': APPLICATION_NAME,
    }

    # Tracing settings
    TRACER_CONFIG = {
        'logging': True,
        'sampler': {
            'type': 'probabilistic',
            'param': 1,
        },
        'local_agent': {
            'reporting_host': 'jaeger-agent',
        },
    }
    RAVEN_CONFIG = {
        'dsn': os.getenv('SENTRY_URL', None),
        'string_max_length': 100000,
        'processors': (
            'raven.processors.SanitizePasswordsProcessor',
        ),
        'release': 'stable',
    }

else:
    TRACER_CONFIG = {
        'logging': False,
        'sampler': {
            'type': 'const',
            'param': 0,
        },
    }
