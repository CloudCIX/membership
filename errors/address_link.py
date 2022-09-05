"""
Error Codes for all of the Methods in the Address Link Service
"""

# Create
membership_address_link_create_001 = (
    'The "address_id" path parameter is invalid. "address_id" must belong to a valid Address record.'
)
membership_address_link_create_101 = (
    'The "reference" parameter is invalid. "reference" cannot be longer than 20 characters.'
)
membership_address_link_create_102 = 'The "territory_id" parameter is invalid. "territory_id" must be an integer.'
membership_address_link_create_103 = (
    'The "territory_id" parameter is invalid. "territory_id" must belong to a valid Territory.'
)
membership_address_link_create_104 = (
    'The "territory_id" parameter is invalid. "territory_id" must belong to a Territory in your Member.'
)
membership_address_link_create_105 = (
    'The "credit_limit" parameter is invalid. "credit_limit" must either be a string representing a Decimal number, '
    'or None'
)
membership_address_link_create_106 = 'The "client" parameter is invalid. "client" must be a boolean.'
membership_address_link_create_107 = 'The "cloud_customer" parameter is invalid. "cloud_customer" must be a boolean.'
membership_address_link_create_108 = (
    'The "cloud_customer" parameter is invalid. As your Address is not a cloud_region you cannot have a '
    'cloud_customer relationship with a partner Address. For more information on how to become a cloud_region '
    'please email sales@cloudcix.com.'
)
membership_address_link_create_109 = 'The "customer" parameter is invalid. "customer" must be a boolean.'
membership_address_link_create_110 = 'The "service_centre" parameter is invalid. "service_centre" must be a boolean.'
membership_address_link_create_111 = 'The "supplier" parameter is invalid. "supplier" must be a boolean.'
membership_address_link_create_112 = 'The "warrantor" parameter is invalid. "warrantor" must be a boolean.'
membership_address_link_create_113 = 'The "extra" parameter is invalid. "extra" must be a dictionary.'
membership_address_link_create_201 = (
    'You do not have permission to execute this method. Your Member is not self-managed.'
)
membership_address_link_create_202 = (
    'You do not have permission to execute this method. An Address Link to the specified Address already exists.'
)

# Read
membership_address_link_read_001 = (
    'The "address_id" path parameter is invalid. "address_id" must belong to a valid Address record that is linked to '
    'your Address.'
)

# Update
membership_address_link_update_001 = (
    'The "address_id" path parameter is invalid. "address_id" must belong to a valid Address record that is linked to '
    'your Address.'
)
membership_address_link_update_101 = (
    'The "reference" parameter is invalid. "reference" cannot be longer than 20 characters.'
)
membership_address_link_update_102 = 'The "territory_id" parameter is invalid. "territory_id" must be an integer.'
membership_address_link_update_103 = (
    'The "territory_id" parameter is invalid. "territory_id" must belong to a valid Territory.'
)
membership_address_link_update_104 = (
    'The "territory_id" parameter is invalid. "territory_id" must belong to a Territory in your Member.'
)
membership_address_link_update_105 = (
    'The "credit_limit" parameter is invalid. "credit_limit" must either be a string representing a Decimal number, '
    'or None'
)
membership_address_link_update_106 = 'The "client" parameter is invalid. "client" must be a boolean.'
membership_address_link_update_107 = 'The "cloud_customer" parameter is invalid. "cloud_customer" must be a boolean.'
membership_address_link_update_108 = (
    'The "cloud_customer" parameter is invalid. As your Address is not a cloud_region you cannot have a '
    'cloud_customer relationship with a partner Address. For more information on how to become a cloud_region '
    'please email sales@cloudcix.com.'
)
membership_address_link_update_109 = 'The "consumer" parameter is invalid. "consumer" must be a boolean.'
membership_address_link_update_110 = 'The "service_centre" parameter is invalid. "service_centre" must be a boolean.'
membership_address_link_update_111 = 'The "supplier" parameter is invalid. "supplier" must be a boolean.'
membership_address_link_update_112 = 'The "warrantor" parameter is invalid. "warrantor" must be a boolean.'
membership_address_link_update_113 = 'The "extra" parameter is invalid. "extra" must be a dictionary.'
membership_address_link_update_201 = (
    'You do not have permission to execute this method. Your Member is not self-managed.'
)
