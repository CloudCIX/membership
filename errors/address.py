"""
Error Codes for all of the Methods in the Address Service
"""

# List
membership_address_list_001 = (
    'One or more of the sent search fields contains invalid values. Please check the sent parameters and ensure they '
    'match the required patterns.'
)

# Create
membership_address_create_101 = 'The "member_id" parameter is invalid. "member_id" is required and must be an integer.'
membership_address_create_102 = 'The "member_id" parameter is invalid. "member_id" must belong to a valid Member.'
membership_address_create_103 = 'The "name" parameter is invalid. "name" is required and must be a string.'
membership_address_create_104 = 'The "name" parameter is invalid. "name" cannot be longer than 250 characters.'
membership_address_create_105 = 'The "address1" parameter is invalid. "address1" is required and must be a string.'
membership_address_create_106 = 'The "address1" parameter is invalid. "address1" cannot be longer than 100 characters.'
membership_address_create_107 = 'The "address2" parameter is invalid. "address2" cannot be longer than 100 characters.'
membership_address_create_108 = 'The "address3" parameter is invalid. "address3" cannot be longer than 100 characters.'
membership_address_create_109 = 'The "city" parameter is invalid. "city" is required and must be a string.'
membership_address_create_110 = 'The "city" parameter is invalid. "city" cannot be longer than 50 characters.'
membership_address_create_111 = (
    'The "country_id" parameter is invalid. "country_id" is required and  must be an integer.'
)
membership_address_create_112 = 'The "country_id" parameter is invalid. "country_id" must belong to a valid Country.'
membership_address_create_113 = 'The "subdivision_id" parameter is invalid. "subdivision_id" must be an integer.'
membership_address_create_114 = (
    'The "subdivision_id" parameter is invalid. "subdivision_id" must belong to a valid Subdivision in the chosen '
    'Country.'
)
membership_address_create_115 = 'The "postcode" parameter is invalid. "postcode" cannot be longer than 20 characters.'
membership_address_create_116 = 'The "phones" parameter is invalid. "phones" must be an array.'
membership_address_create_117 = 'The "phones" parameter is invalid. Each item in the array must be an object.'
membership_address_create_118 = (
    'The "phones" parameter is invalid. Each item in the array must have both the "name" and "number" keys.'
)
membership_address_create_119 = (
    'The "phones" parameter is invalid. One of the sent values for "number" is not a valid phone number.'
)
membership_address_create_120 = 'The "email" parameter is invalid. "email" cannot be longer than 255 characters.'
membership_address_create_121 = 'The "website" parameter is invalid. "website" cannot be longer than 50 characters.'
membership_address_create_122 = 'The "gln" parameter is invalid. "gln" cannot be longer than 13 characters.'
membership_address_create_123 = (
    'The "vat_number" parameter is invalid. "vat_number" cannot be longer than 20 characters.'
)
membership_address_create_124 = (
    'The "language_id" parameter is invalid. "language_id" is required and must be an integer.'
)
membership_address_create_125 = 'The "language_id" parameter is invalid. "language_id" must belong to a valid Language.'
membership_address_create_126 = (
    'The "currency_id" parameter is invalid. "currency_id" is required and must be an integer.'
)
membership_address_create_127 = 'The "currency_id" parameter is invalid. "currency_id" must belong to a valid Currency.'
membership_address_create_128 = (
    'The "billing_address_id" parameter is invalid. "billing_address_id" must be an integer.'
)
membership_address_create_129 = (
    'The "billing_address_id" parameter is invalid. "billing_address_id" must belong to a valid Address in the '
    'specified Member.'
)
membership_address_create_201 = 'You do not have permission to make this request. Your Member must be self-managed.'
membership_address_create_202 = (
    'You do not have permission to make this request. You are attempting to make an Address in another self-managed '
    'Member.'
)

# Read
membership_address_read_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Address record.'
membership_address_read_201 = (
    'You do not have permission to make this request. Your Address must be linked to the Address you want to read.'
)

# Update
membership_address_update_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Address record.'
membership_address_update_101 = 'The "name" parameter is invalid. "name" is required and must be a string.'
membership_address_update_102 = 'The "name" parameter is invalid. "name" cannot be longer than 250 characters.'
membership_address_update_103 = 'The "address1" parameter is invalid. "address1" is required and must be a string.'
membership_address_update_104 = 'The "address1" parameter is invalid. "address1" cannot be longer than 100 characters.'
membership_address_update_105 = 'The "address2" parameter is invalid. "address2" cannot be longer than 100 characters.'
membership_address_update_106 = 'The "address3" parameter is invalid. "address3" cannot be longer than 100 characters.'
membership_address_update_107 = 'The "city" parameter is invalid. "city" is required and must be a string.'
membership_address_update_108 = 'The "city" parameter is invalid. "city" cannot be longer than 50 characters.'
membership_address_update_109 = (
    'The "country_id" parameter is invalid. "country_id" is required and  must be an integer.'
)
membership_address_update_110 = 'The "country_id" parameter is invalid. "country_id" must belong to a valid Country.'
membership_address_update_111 = 'The "subdivision_id" parameter is invalid. "subdivision_id" must be an integer.'
membership_address_update_112 = (
    'The "subdivision_id" parameter is invalid. "subdivision_id" must belong to a valid Subdivision in the chosen '
    'Country.'
)
membership_address_update_113 = 'The "postcode" parameter is invalid. "postcode" cannot be longer than 20 characters.'
membership_address_update_114 = 'The "phones" parameter is invalid. "phones" must be an array.'
membership_address_update_115 = 'The "phones" parameter is invalid. Each item in the array must be an object.'
membership_address_update_116 = (
    'The "phones" parameter is invalid. Each item in the array must have both the "name" and "number" keys.'
)
membership_address_update_117 = (
    'The "phones" parameter is invalid. One of the sent values for "number" is not a valid phone number.'
)
membership_address_update_118 = 'The "email" parameter is invalid. "email" cannot be longer than 255 characters.'
membership_address_update_119 = 'The "website" parameter is invalid. "website" cannot be longer than 50 characters.'
membership_address_update_120 = 'The "gln" parameter is invalid. "gln" cannot be longer than 13 characters.'
membership_address_update_121 = (
    'The "vat_number" parameter is invalid. "vat_number" cannot be longer than 20 characters.'
)
membership_address_update_122 = (
    'The "language_id" parameter is invalid. "language_id" is required and must be an integer.'
)
membership_address_update_123 = 'The "language_id" parameter is invalid. "language_id" must belong to a valid Language.'
membership_address_update_124 = (
    'The "currency_id" parameter is invalid. "currency_id" is required and must be an integer.'
)
membership_address_update_125 = 'The "currency_id" parameter is invalid. "currency_id" must belong to a valid Currency.'
membership_address_update_126 = (
    'The "billing_address_id" parameter is invalid. "billing_address_id" must be an integer.'
)
membership_address_update_127 = (
    'The "billing_address_id" parameter is invalid. "billing_address_id" must belong to a valid Address in the '
    'specified Member.'
)
membership_address_update_128 = 'The "cloud_region" parameter is invalid. "cloud_region" must be a boolean.'
membership_address_update_129 = (
    'The "cloud_region" parameter is invalid. The address member can only have the role cloud_region if they are '
    'self-managed.'
)
membership_address_update_201 = (
    'You do not have permission to execute this method. Only Member 1 administrator\'s can change the role of an '
    'Address.'
)
membership_address_update_202 = 'You do not have permission to make this request. Your Member must be self-managed.'
membership_address_update_203 = (
    'You do not have permission to make this request. You are attempting to make an Address in another self-managed '
    'Member.'
)
membership_address_update_204 = (
    'You do not have permission to make this request. Your Address must be linked to the Address you are trying to '
    'update.'
)

# Verbose List
membership_verbose_address_list_001 = (
    'One or more of the sent search fields contains invalid values. Please check the sent parameters and ensure they '
    'match the required patterns.'
)
