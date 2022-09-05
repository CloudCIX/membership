"""
Error Codes for all of the Methods in the Auth Service
"""

# Create
membership_token_create_001 = 'Both the "email" and "password" keys are required in the sent data.'
membership_token_create_002 = 'The sent email and password combination is invalid. Please check both and try again.'
membership_token_create_003 = (
    'The sent "api_key" is invalid. The authenticating User does not belong to a Member with that "api_key"'
)
membership_token_create_004 = (
    'The "first_otp" is required. Please contact the administrator of your account to receive if you have not been '
    'provided it by them.'
)
membership_token_create_005 = (
    'The "first_otp" is incorrect. Please contact the administrator of your account to confirm the value'
)
membership_token_create_006 = (
    'The "first_otp" is required. Please contact the administrator of your account to confirm the value'
)
membership_token_create_007 = 'One Time Password (otp) is required. Please check your Authenticator App and try again.'
membership_token_create_008 = 'One Time Password (otp) is invalid. Please check your Authenticator App and try again.'
# Update
membership_token_update_001 = (
    'The authentication token used to make this request was already invalid. Please generate a new token from scratch '
    'instead.'
)
