"""
Error Codes for all of the Methods in the Profile Service
"""

# Create
membership_profile_create_101 = 'The "name" parameter is invalid. "name" is required and must be a string.'
membership_profile_create_102 = 'The "name" parameter is invalid. "name" cannot be longer than 50 characters.'
membership_profile_create_103 = (
    'The "name" parameter is invalid. A Profile with that name already exists for your Member.'
)
membership_profile_create_201 = 'You do not have permission to make this request. Your Member must be self-managed.'
membership_profile_create_202 = 'You do not have permission to make this request. You must be an administrator.'

# Read
membership_profile_read_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Profile record.'

# Update
membership_profile_update_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Profile record.'
membership_profile_update_101 = 'The "name" parameter is invalid. "name" is required and must be a string.'
membership_profile_update_102 = 'The "name" parameter is invalid. "name" cannot be longer than 50 characters.'
membership_profile_update_103 = (
    'The "name" parameter is invalid. A Profile with that name already exists for your Member.'
)
membership_profile_update_201 = 'You do not have permission to make this request. Your Member must be self-managed.'
membership_profile_update_202 = 'You do not have permission to make this request. You must be an administrator.'

# Delete
membership_profile_delete_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Profile record.'
membership_profile_delete_201 = 'You do not have permission to make this request. Your Member must be self-managed.'
membership_profile_delete_202 = 'You do not have permission to make this request. You must be an administrator.'
membership_profile_delete_203 = (
    'You do not have permission to make this request. The specified Profile is not empty.'
)
