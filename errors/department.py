"""
Error Codes for all of the Methods in the Department Service
"""

# Create
membership_department_create_101 = 'The "name" parameter is invalid. "name" is required and must be a string.'
membership_department_create_102 = 'The "name" parameter is invalid. "name" cannot be longer than 50 characters.'
membership_department_create_103 = (
    'The "name" parameter is invalid. A Department with that name already exists for your Member.'
)
membership_department_create_201 = 'You do not have permission to make this request. Your Member must be self-managed.'
membership_department_create_202 = 'You do not have permission to make this request. You must be an administrator.'

# Read
membership_department_read_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Department record.'

# Update
membership_department_update_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Department record.'
membership_department_update_101 = 'The "name" parameter is invalid. "name" is required and must be a string.'
membership_department_update_102 = 'The "name" parameter is invalid. "name" cannot be longer than 50 characters.'
membership_department_update_103 = (
    'The "name" parameter is invalid. A Department with that name already exists for your Member.'
)
membership_department_update_201 = 'You do not have permission to make this request. Your Member must be self-managed.'
membership_department_update_202 = 'You do not have permission to make this request. You must be an administrator.'

# Delete
membership_department_delete_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Department record.'
membership_department_delete_201 = 'You do not have permission to make this request. Your Member must be self-managed.'
membership_department_delete_202 = 'You do not have permission to make this request. You must be an administrator.'
membership_department_delete_203 = (
    'You do not have permission to make this request. The specified Department is not empty.'
)
