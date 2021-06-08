# libs
import serpy


__all__ = [
    'MemberLinkSerializer',
]


class MemberLinkSerializer(serpy.Serializer):
    """
    contra_member_id:
        description: The id of the Member that the Link was made to
        type: integer
    member_id:
        description: The id of the Member that made the Link
        type: integer
    uri:
        description: The absolute URL of the Member Link that can be used to perform `Read` operations on it
        type: string
    """
    contra_member_id = serpy.Field()
    member_id = serpy.Field()
    uri = serpy.Field(attr='get_absolute_url', call=True)

    # Backwards Compatibility
    old_contra_member_id = serpy.Field(attr='contra_member_id', label='idMemberContra')
    old_member_id = serpy.Field(attr='member_id', label='idMember')
