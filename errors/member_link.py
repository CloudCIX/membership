"""
Error Codes for all of the Methods in the Member Link Service
"""

# List
membership_member_link_list_001 = (
    'The "member_id" path parameter is invalid. "member_id" must belong to a valid Member record.'
)
membership_member_link_list_002 = (
    'One or more of the sent search fields contains invalid values. Please check the sent parameters and ensure they '
    'match the required patterns.'
)

# Read
membership_member_link_read_001 = (
    'One or more of the path parameters are invalid. The combination of "member_id" and "contra_member_id" does not '
    'correspond to an existing Member Link.'
)
