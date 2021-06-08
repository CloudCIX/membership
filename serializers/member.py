# libs
import serpy
# local
from membership.serializers.currency import CurrencySerializer


__all__ = [
    'MemberSerializer',
]


class MemberSerializer(serpy.Serializer):
    """
    api_key:
        description: The api_key of the Member that is used to make generate tokens to make API requests to CloudCIX
        type: string
    currency:
        $ref: '#/components/schemas/Currency'
    gln_prefix:
        description: The Global Location Number Prefix used by the Member for its Addresses
        type: string
    id:
        description: The id of the Member
        type: integer
    name:
        description: The name of the Member
        type: string
    secret:
        description: |
            A flag stating whether the Member is secret or not. A secret member is only visible to their partner Member
            and cannot be self-managed
        type: boolean
    self_managed:
        description: A flag stating whether the Member is self-managed or not
        type: boolean
    uri:
        description: The absolute URL of the Member that can be used to perform `Read` and `Update` operations on it
        type: string
    """
    api_key = serpy.Field()
    currency = CurrencySerializer()
    gln_prefix = serpy.Field(required=False)
    id = serpy.Field()
    name = serpy.Field()
    secret = serpy.Field()
    self_managed = serpy.Field()
    uri = serpy.Field(attr='get_absolute_url', call=True)

    # Backwards Compatibility
    old_currency_id = serpy.Field(attr='currency_id', label='idCurrency')
    old_gln_prefix = serpy.Field(attr='gln_prefix', label='glnPrefix')
    old_id = serpy.Field(attr='pk', label='idMember')
    old_name = serpy.Field(attr='name', label='groupName')
    old_self_managed = serpy.Field(attr='self_managed', label='selfManaged')
