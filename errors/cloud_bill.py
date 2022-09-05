"""
Error Codes for the CloudBill read method
"""
membership_cloud_bill_read_001 = (
    'One of the sent "address_id" or "target_address_id" does not exist. Please send valid address IDs in request.'
)
membership_cloud_bill_read_002 = (
    'There is no AddressLink between the two specified Addresses or any Addresses in the sent "address_id" Member and'
    ' the "target_address_id".'
)
membership_cloud_bill_read_201 = (
    'You do not have permission to make this request. You can only read cloud bill records where your address is '
    'either the "address_id" or "target_address_id".'
)
