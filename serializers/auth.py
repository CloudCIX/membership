"""
Dummy Auth Serializer to generate the Auth schema
"""
# libs
import serpy


class AuthSerializer(serpy.Serializer):
    """
    token:
      description: The token generated for the User that is valid for the next hour
      type: string
    """
    token = serpy.Field()
