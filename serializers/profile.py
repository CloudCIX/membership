# libs
import serpy
# local
from membership.serializers.member import MemberSerializer


__all__ = [
    'ProfileSerializer',
]


class ProfileSerializer(serpy.Serializer):
    """
    id:
        description: The id of the Profile
        type: integer
    member:
        $ref: '#/components/schemas/Member'
    name:
        description: The name of the Profile
        type: string
    uri:
        description: |
            The absolute URL of the Profile that can be used to perform `Read`, `Update` and `Delete` operations on it
        type: string
    """
    id = serpy.Field()
    member = MemberSerializer()
    name = serpy.Field()
    uri = serpy.Field(attr='get_absolute_url', call=True)

    # Backwards Compatibility
    old_id = serpy.Field(attr='id', label='idProfile')
    old_member_id = serpy.Field(attr='member_id', label='idMember')
