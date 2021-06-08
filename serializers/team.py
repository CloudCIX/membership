# libs
import serpy
# local
from membership.serializers.member import MemberSerializer
from membership.serializers.user import UserSerializer


class TeamSerializer(serpy.Serializer):
    """
    id:
        description: The id of the Team
        type: integer
    member:
        $ref: '#/components/schemas/Member'
    name:
        description: The name of the team
        type: string
    uri:
        description: |
            The absolute URL of the Team that can be used to perform `Read`, `Update` and `Delete` operations on it
        type: string
    users:
        $ref: '#/components/schemas/User'
    """
    id = serpy.Field()
    member = MemberSerializer()
    name = serpy.Field()
    uri = serpy.Field(attr='get_absolute_url', call=True)
    users = UserSerializer(attr='users.all', call=True, many=True)

    # backwards compat
    old_member_id = serpy.Field(attr='member_id', label='idMember')
