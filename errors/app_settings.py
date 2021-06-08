"""
Error Codes for all of the Methods in the App Settings Service
"""

# Create
membership_app_settings_create_001 = (
    'An App Settings record already exists. Please update the existing record if required.'
)
membership_app_settings_create_101 = (
    'The "minio_access_key" parameter is invalid. "minio_access_key" cannot be longer than 100 characters.'
)
membership_app_settings_create_102 = (
    'The "minio_secret_key" parameter is invalid. "minio_secret_key" cannot be longer than 100 characters.'
)
membership_app_settings_create_103 = (
    'The "minio_url" parameter is invalid. "minio_url" cannot be longer than 240 characters.'
)
membership_app_settings_create_104 = (
    'The "minio_url" parameter is invalid. Each segment of "minio_url" separated by "." characters cannot be longer '
    'than 63 characters.'
)
membership_app_settings_create_201 = 'You do not have permission to make this request'

# Read
membership_app_settings_read_001 = (
    'The "pk" path parameter is invalid. "pk" must belong to a valid App Settings record.'
)
membership_app_settings_read_201 = 'You do not have permission to make this request'

# Update
membership_app_settings_update_001 = (
    'The "pk" path parameter is invalid. "pk" must belong to a valid App Settings record.'
)
membership_app_settings_update_101 = (
    'The "minio_access_key" parameter is invalid. "minio_access_key" cannot be longer than 100 characters.'
)
membership_app_settings_update_102 = (
    'The "minio_secret_key" parameter is invalid. "minio_secret_key" cannot be longer than 100 characters.'
)
membership_app_settings_update_103 = (
    'The "minio_url" parameter is invalid. "minio_url" cannot be longer than 240 characters.'
)
membership_app_settings_update_104 = (
    'The "minio_url" parameter is invalid. Each segment of "minio_url" separated by "." characters cannot be longer '
    'than 63 characters.'
)

membership_app_settings_update_201 = 'You do not have permission to make this request'

# Delete
membership_app_settings_delete_001 = (
    'The "pk" path parameter is invalid. "pk" must belong to a valid App Settings record.'
)
membership_app_settings_delete_201 = 'You do not have permission to make this request'
