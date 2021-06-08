"""
Error Codes for all of the Methods in the Subdivision Service
"""

# List
membership_subdivision_list_001 = (
    'The "country_id" path parameter is invalid. "country_id" must belong to a valid Country record.'
)
membership_subdivision_list_002 = (
    'One or more of the sent search fields contains invalid values. Please check the sent parameters and ensure they '
    'match the required patterns.'
)

# Read
membership_subdivision_read_001 = (
    'One or both of the path parameters are invalid. The combination of "country_id" and "id" does not belong to '
    'a valid Subdivision. Check your parameters and try again.'
)
