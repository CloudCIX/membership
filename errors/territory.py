"""
Error Codes for all of the Methods in the Territory Service
"""

# Create
membership_territory_create_101 = 'The "name" parameter is invalid. "name" is required and must be a string.'
membership_territory_create_102 = 'The "name" parameter is invalid. "name" cannot be longer than 50 characters.'
membership_territory_create_103 = (
    'The "name" parameter is invalid. A Territory with that name already exists for your Member.'
)
membership_territory_create_201 = 'You do not have permission to make this request. Your Member must be self-managed.'
membership_territory_create_202 = 'You do not have permission to make this request. You must be an administrator.'

# Read
membership_territory_read_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Territory record.'

# Update
membership_territory_update_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Territory record.'
membership_territory_update_101 = 'The "name" parameter is invalid. "name" is required and must be a string.'
membership_territory_update_102 = 'The "name" parameter is invalid. "name" cannot be longer than 50 characters.'
membership_territory_update_103 = (
    'The "name" parameter is invalid. A Territory with that name already exists for your Member.'
)
membership_territory_update_201 = 'You do not have permission to make this request. Your Member must be self-managed.'
membership_territory_update_202 = 'You do not have permission to make this request. You must be an administrator.'

# Delete
membership_territory_delete_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Territory record.'
membership_territory_delete_201 = 'You do not have permission to make this request. Your Member must be self-managed.'
membership_territory_delete_202 = 'You do not have permission to make this request. You must be an administrator.'
membership_territory_delete_203 = (
    'You do not have permission to make this request. The specified Territory is in use in at least one Address Link.'
)
