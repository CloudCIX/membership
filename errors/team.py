"""
Error Codes for all of the Methods in the Team Service
"""

# Create
membership_team_create_101 = 'The "name" parameter is invalid. "name" is required and must be a string.'
membership_team_create_102 = 'The "name" parameter is invalid. "name" cannot be longer than 50 characters.'
membership_team_create_103 = (
    'The "users" parameter is invalid. "users" must be an array of integers representing User ids.'
)
membership_team_create_104 = (
    'The "users" parameter is invalid. One or more of the sent ids do not correspond to Users in your Member.'
)
membership_team_create_201 = 'You do not have permission to make this request. Your Member must be self-managed.'
membership_team_create_202 = 'You do not have permission to make this request. You must be an administrator.'

# Read
membership_team_read_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Team record.'

# Update
membership_team_update_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Team record.'
membership_team_update_101 = 'The "name" parameter is invalid. "name" is required and must be a string.'
membership_team_update_102 = 'The "name" parameter is invalid. "name" cannot be longer than 50 characters.'
membership_team_update_103 = (
    'The "users" parameter is invalid. "users" must be an array of integers representing User ids.'
)
membership_team_update_104 = (
    'The "users" parameter is invalid. One or more of the sent ids do not correspond to Users in your Member.'
)
membership_team_update_201 = 'You do not have permission to make this request. Your Member must be self-managed.'
membership_team_update_202 = 'You do not have permission to make this request. You must be an administrator.'

# Delete
membership_team_delete_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Team record.'
membership_team_delete_201 = 'You do not have permission to make this request. Your Member must be self-managed.'
membership_team_delete_202 = 'You do not have permission to make this request. You must be an administrator.'
