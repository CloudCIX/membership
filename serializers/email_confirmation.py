"""
Dummy Email Confirmation Serializer
"""
# libs
import serpy


class EmailConfirmationSerializer(serpy.Serializer):
    """
    valid:
        description: Response if Email Confirmation Token is valid for the sent email_token and user_id
        type: boolean
    """
    valid = serpy.Field()
