"""
Error Codes for all of the Methods in the User Service
"""

# List
membership_user_list_001 = (
    'One or more of the sent search fields contains invalid values. Please check the sent parameters and ensure they '
    'match the required patterns.'
)

# Create
membership_user_create_001 = (
    'Unable to create User in LDAP. An unexpected error occured, please try again later or contact CloudCIX if this '
    'continues.'
)
membership_user_create_002 = (
    'Unable to send confirmation email. Please try again later or contact CIX if this continues.'
)
membership_user_create_101 = 'The "address_id" parameter is invalid. "address_id" is required and must be an integer.'
membership_user_create_102 = (
    'The "address_id" parameter is invalid. "address_id" must belong to a valid Address.'
)
membership_user_create_103 = (
    'The "address_id" parameter is invalid. "address_id" must belong to an Address that is linked to your Address'
)
membership_user_create_104 = 'The "first_name" parameter is invalid. "first_name" is required and must be a string.'
membership_user_create_105 = 'The "first_name" parameter is invalid. "first_name" cannot be longer than 50 characters.'
membership_user_create_106 = 'The "surname" parameter is invalid. "surname" is required and must be a string.'
membership_user_create_107 = 'The "surname" parameter is invalid. "surname" cannot be longer than 50 characters.'
membership_user_create_108 = 'The "email" parameter is invalid. "email" is required and must be a string.'
membership_user_create_109 = 'The "email" parameter is invalid. "email" cannot be longer than 255 characters.'
membership_user_create_110 = 'The "email" parameter is invalid. "email" must be a valid email.'
membership_user_create_111 = (
    'The "email" parameter is invalid. There is another User in the specified Member with the specified "email"'
)
membership_user_create_112 = 'The "password" parameter is invalid. "password" is required and must be a string.'
membership_user_create_113 = 'The "global_user" parameter is invalid. "global_user" must be a boolean.'
membership_user_create_114 = 'The "global_active" parameter is invalid. "global_active" must be a boolean.'
membership_user_create_115 = 'The "is_private" parameter is invalid. "is_private" must be a boolean.'
membership_user_create_116 = (
    'The "timezone" parameter is invalid. "timezone" is required and must be a string containing the name of a valid '
    'Timezone.'
)
membership_user_create_117 = (
    'The "start_date" parameter is invalid. "start_date" is required and must be a date in ISO format.'
)
membership_user_create_118 = (
    'The "expiry_date" parameter is invalid. "expiry_date" is required and must be a date in ISO format.'
)
membership_user_create_119 = (
    'The "expiry_date" parameter is invalid. "expiry_date" cannot be before the specified "start_date".'
)
membership_user_create_120 = (
    'The "expiry_date" parameter is invalid. "expiry_date" cannot be set to a date in the past.'
)
membership_user_create_121 = 'The "language_id" parameter is invalid. "language_id" is required and must be an integer.'
membership_user_create_122 = 'The "language_id" parameter is invalid. "language_id" must belong to a valid Language.'
membership_user_create_123 = 'The "profile_id" parameter is invalid. "profile_id" must be an integer.'
membership_user_create_124 = (
    'The "profile_id" parameter is invalid. "profile_id" must belong to a valid Profile in the specified Address\' '
    'Member.'
)
membership_user_create_125 = 'The "department_id" parameter is invalid. "department_id" must be an integer.'
membership_user_create_126 = (
    'The "department_id" parameter is invalid. "department_id" must belong to a valid Department in the specified '
    "Address' Member."
)
membership_user_create_127 = 'The "job_title" parameter is invalid. "job_title" cannot be longer than 100 characters.'
membership_user_create_128 = (
    'The "notifications" parameter is invalid. "notifications" must be an array of objects that all contain at least '
    'the "transaction_type_id" key which represents the ids of Transaction Types that the User is to be notified about.'
)
membership_user_create_129 = (
    'The "notifications" parameter is invalid. One or more of the sent ids do not correspond with valid Transaction '
    'Type records.'
)
membership_user_create_130 = 'The "phones" parameter is invalid. "phones" must be an array.'
membership_user_create_131 = 'The "phones" parameter is invalid. Each item in the array must be an object.'
membership_user_create_132 = (
    'The "phones" parameter is invalid. Each item in the array must have both the "name" and "number" keys.'
)
membership_user_create_133 = (
    'The "phones" parameter is invalid. One of the sent values for "number" is not a valid phone number.'
)
membership_user_create_134 = (
    'The "image" parameter is invalid. If "image" is an object, it must have both the "name" and "data" keys.'
)
membership_user_create_135 = (
    'The "image" parameter is invalid. The value for the "data" key should contain an image encoded in base64.'
)
membership_user_create_136 = (
    'The "image" parameter is invalid. The value for the "data" key cannot be empty.'
)
membership_user_create_137 = (
    'The "image" parameter is invalid. "image" must either be an object or a string representing a URL where the image '
    'is hosted, if not hosting it in CloudCIX.'
)
membership_user_create_138 = (
    'The "otp" parameter is invalid. "otp" must be a boolean.'
)

membership_user_create_201 = 'You do not have permission to execute this method. Your Member must be self-managed.'
membership_user_create_202 = (
    'You do not have permission to execute this method. The specified Address must be in your Member, or a non '
    'self-managed partner Member.'
)
membership_user_create_203 = 'You do not have permission to execute this method. You must be an administrator.'

# Read
membership_user_read_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid User record.'
membership_user_read_201 = (
    'You do not have permission to execute this method. The specified User belongs to a  a Self Managed Partner Member '
    'and has expired.'
)
membership_user_read_202 = (
    'You do not have permission to execute this method. The specified User belongs to a Self Managed Partner Member and'
    ' their account is private.'
)
membership_user_read_203 = (
    "You do not have permission to execute this method. Your Address is not linked to the specified User's Address, "
    'and the specified User is not in your Member.'
)
membership_user_read_204 = (
    "You do not have permission to execute this method. You Address is not linked to the specified User's Address, "
    'and you are not a global User.'
)

# Update
membership_user_update_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid User record.'
membership_user_update_002 = (
    '"password" is required and must be a string. To create an LDAP entry for user a password is required.'
)
membership_user_update_003 = (
    'Unable to update User in LDAP.  An unexpected error occured, please try again later or contact CloudCIX if this '
    'continues.'
)
membership_user_update_101 = 'The "address_id" parameter is invalid. "address_id" is required and must be an integer.'
membership_user_update_102 = 'The "address_id" parameter is invalid. "address_id" must belong to a valid Address.'
membership_user_update_103 = (
    'The "address_id" parameter is invalid. "address_id" must belong to an Address that is linked to your Address'
)
membership_user_update_104 = (
    'The "address_id" parameter is invalid. "address_id" belongs to an Address outside of the User\'s original Member.'
)
membership_user_update_105 = 'The "first_name" parameter is invalid. "first_name" is required and must be a string.'
membership_user_update_106 = 'The "first_name" parameter is invalid. "first_name" cannot be longer than 50 characters.'
membership_user_update_107 = 'The "surname" parameter is invalid. "surname" is required and must be a string.'
membership_user_update_108 = 'The "surname" parameter is invalid. "surname" cannot be longer than 50 characters.'
membership_user_update_109 = 'The "email" parameter is invalid. "email" is required and must be a string.'
membership_user_update_110 = 'The "email" parameter is invalid. "email" cannot be longer than 255 characters.'
membership_user_update_111 = 'The "email" parameter is invalid. "email" must be a valid email.'
membership_user_update_112 = (
    'The "email" parameter is invalid. There is another User in the specified Member with the specified "email"'
)
membership_user_update_113 = 'The "global_user" parameter is invalid. "global_user" must be a boolean.'
membership_user_update_114 = 'The "global_active" parameter is invalid. "global_active" must be a boolean.'
membership_user_update_115 = 'The "is_private" parameter is invalid. "is_private" must be a boolean.'
membership_user_update_116 = (
    'The "timezone" parameter is invalid. "timezone" is required and must be a string containing the name of a valid '
    'Timezone.'
)
membership_user_update_117 = (
    'The "start_date" parameter is invalid. "start_date" is required and must be a date in ISO format.'
)
membership_user_update_118 = (
    'The "expiry_date" parameter is invalid. "expiry_date" is required and must be a date in ISO format.'
)
membership_user_update_119 = (
    'The "expiry_date" parameter is invalid. "expiry_date" cannot be before the newly specified "start_date".'
)
membership_user_update_120 = (
    'The "expiry_date" parameter is invalid. "expiry_date" cannot be before the original "start_date".'
)

membership_user_update_121 = 'The "language_id" parameter is invalid. "language_id" is required and must be an integer.'
membership_user_update_122 = 'The "language_id" parameter is invalid. "language_id" must belong to a valid Language.'
membership_user_update_123 = 'The "profile_id" parameter is invalid. "profile_id" must be an integer.'
membership_user_update_124 = (
    'The "profile_id" parameter is invalid. "profile_id" must belong to a valid Profile in the specified Address\' '
    'Member.'
)
membership_user_update_125 = 'The "department_id" parameter is invalid. "department_id" must be an integer.'
membership_user_update_126 = (
    'The "department_id" parameter is invalid. "department_id" must belong to a valid Department in the specified '
    "Address' Member."
)
membership_user_update_127 = 'The "job_title" parameter is invalid. "job_title" cannot be longer than 100 characters.'
membership_user_update_128 = (
    'The "notifications" parameter is invalid. "notifications" must be an array of objects that all contain at least '
    'the "transaction_type_id" key which represents the ids of Transaction Types that the User is to be notified about.'
)
membership_user_update_129 = (
    'The "notifications" parameter is invalid. One or more of the sent ids do not correspond with valid Transaction '
    'Type records.'
)
membership_user_update_130 = 'The "phones" parameter is invalid. "phones" must be an array.'
membership_user_update_131 = 'The "phones" parameter is invalid. Each item in the array must be an object.'
membership_user_update_132 = (
    'The "phones" parameter is invalid. Each item in the array must have both the "name" and "number" keys.'
)
membership_user_update_133 = (
    'The "phones" parameter is invalid. One of the sent values for "number" is not a valid phone number.'
)
membership_user_update_134 = (
    'The "image" parameter is invalid. If "image" is an object, it must have both the "name" and "data" keys.'
)
membership_user_update_135 = (
    'The "image" parameter is invalid. The value for the "data" key should contain an image encoded in base64.'
)
membership_user_update_136 = (
    'The "image" parameter is invalid. The value for the "data" key cannot be empty.'
)
membership_user_update_137 = (
    'The "image" parameter is invalid. "image" must either be an object or a string representing a URL where the image '
    'is hosted, if not hosting it in CloudCIX.'
)
membership_user_update_138 = (
    'The "otp" parameter is invalid. '
    '"otp" must be a boolean.'
)
membership_user_update_139 = (
    'The "first_otp" parameter is invalid. "first_otp" must be an integer.'
)
membership_user_update_140 = (
    'The "first_otp" parameter is invalid. "first_otp" must be between 100000 and 999999 inclusive.'
)
membership_user_update_141 = (
    'The "first_otp" parameter is invalid. "first_otp" is only allowed if "otp" is true'
)
membership_user_update_142 = 'The "administrator" parameter is invalid. "administrator" must be a boolean.'
membership_user_update_143 = 'The "robot" parameter is invalid. "robot" must be a boolean.'
membership_user_update_144 = (
    'The "robot" parameter is invalid. As the User\'s Address is not a cloud_region, the user cannot have a robot '
    'status'
)
membership_user_update_145 = 'The "robot" parameter is invalid. A robot User already exists in the User\'s Address.'
membership_user_update_146 = 'The "otp" parameter is invalid. OTP cannot be turned on for robot or API users.'

membership_user_update_201 = (
    "You do not have permission to execute this method. Only Member 1 administrator's can change the roles of a User."
)
membership_user_update_202 = 'You do not have permission to execute this method. Your Member must be self-managed.'
membership_user_update_203 = (
    'You do not have permission to execute this method. The specified User should be in your Member. If you are a '
    'global User, the specified User can also be in one of your linked Addresses.'
)
membership_user_update_204 = (
    'You do not have permission to execute this method. The specified User is in a self-managed partner Member.'
)
membership_user_update_205 = (
    'You do not have permission to execute this method. Only an administrator can update Users other than themselves '
    'in their Member.'
)
membership_user_update_206 = (
    'You do not have permission to execute this method. You can only change your Address if you are an administrator '
    'or you are a global User.'
)
