"""
Error Codes for all of the Methods in the Member Service
"""

# List
membership_member_list_001 = (
    'One or more of the sent search fields contains invalid values. Please check the sent parameters and ensure they '
    'match the required patterns.'
)

# Create
membership_member_create_101 = 'The "name" parameter is invalid. "name" is required and must be a string.'
membership_member_create_102 = 'The "name" parameter is invalid. "name" cannot be longer than 250 characters.'
membership_member_create_103 = (
    'The "currency_id" parameter is invalid. "currency_id" is required and must be an integer.'
)
membership_member_create_104 = 'The "currency_id" parameter is invalid. "currency_id" must belong to a valid Currency.'
membership_member_create_105 = (
    'The "gln_prefix" parameter is invalid. "gln_prefix" cannot be longer than 12 characters.'
)
membership_member_create_106 = 'The "secret" parameter is invalid. "secret" must be a boolean.'
membership_member_create_201 = 'You do not have permission to make this request. Your Member must be self-managed.'

# Read
membership_member_read_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Member record.'
membership_member_read_201 = (
    'You do not have permission to make this request. Your Member is not linked to the specified Member.'
)

# Update
membership_member_update_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Member record.'
membership_member_update_101 = 'The "name" parameter is invalid. "name" is required and must be a string.'
membership_member_update_102 = 'The "name" parameter is invalid. "name" cannot be longer than 250 characters.'
membership_member_update_103 = (
    'The "currency_id" parameter is invalid. "currency_id" is required and must be an integer.'
)
membership_member_update_104 = 'The "currency_id" parameter is invalid. "currency_id" must belong to a valid Currency.'
membership_member_update_105 = (
    'The "gln_prefix" parameter is invalid. "gln_prefix" cannot be longer than 12 characters.'
)
membership_member_update_106 = 'The "self_managed" parameter is invalid. "self_managed" must be a boolean.'
membership_member_update_107 = (
    'The "self_managed" parameter is invalid. You cannot make a self-managed Member non self-managed again.'
)
membership_member_update_108 = 'The "secret" parameter is invalid. "secret" must be a boolean.'
membership_member_update_109 = 'The "secret" parameter is invalid. A "self_managed" Member cannot be a "secret" Member.'
membership_member_update_201 = (
    'You do not have permission to make this request. Check the docs for the permissions required to update a Member '
    'record.'
)
