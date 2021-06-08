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
    'First OTP is required."'
)
membership_token_create_005 = (
    'The one time password is incorrect. Please try again"'
)
membership_token_create_006 = (
    'Both the "otp" and "time" keys are required in the sent data.'
)
membership_token_create_007 = (
    'The sent one Time Password is invalid. Please check and try again'
)

# Update
membership_token_update_001 = (
    'The authentication token used to make this request was already invalid. Please generate a new token from scratch '
    'instead.'
)
