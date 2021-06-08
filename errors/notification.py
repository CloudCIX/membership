"""
Error Codes for all of the Methods in the Notification Service
"""

# List
membership_notification_list_001 = (
    'The "address_id" path parameter is invalid. "address_id" must belong to a valid Address record.'
)
membership_notification_list_002 = (
    'The "transaction_type_id" path parameter is invalid. "transaction_type_id" must belong to a valid Transaction Type'
    ' record.'
)
membership_notification_list_201 = (
    'You do not have permission to make this request. Your Address must be linked to the specified Address.'
)
