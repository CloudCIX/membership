# libs
import serpy
# local
from membership.serializers.territory import TerritorySerializer


__all__ = [
    'AddressLinkSerializer',
]


class AddressLinkSerializer(serpy.Serializer):
    """
    address_id:
        description: The id of the Address that made the Link
        type: integer
    client:
        description: A flag stating if the Contra Address is a client for the Address
        type: boolean
    compute:
        description: A flag stating if the Contra Address can build cloud resources in the Address' region
        type: boolean
    contra_address_id:
        description: The id of the Address that the Link was made to
        type: integer
    credit_limit:
        description: |
            The agreed credit limit for Financials given to the contra address by the address.
            If set, the credit owed by the contra address to the address cannot exceed this amount.
        type: string
        format: decimal
    customer:
        description: A flag stating if the Contra Address is a customer for the Address
        type: boolean
    note:
        description: The note attached to the Link by the Address that made it
        type: string
    reference:
        description: The reference attached to the Link by the Address that made it
        type: string
    service_centre:
        description: A flag stating if the Contra Address is a Service Centre for the Address
        type: boolean
    supplier:
        description: A flag stating if the Contra Address is a Supplier for the Address
        type: boolean
    territory:
        $ref: '#/components/schemas/Territory'
    uri:
        description: The absolute URL of the Address Link that can be used to perform `Read` operations on it
        type: string
    warrantor:
        description: A flag stating if the Contra Address is a Warrantor for the Address
        type: boolean
    """
    address_id = serpy.Field()
    client = serpy.BoolField()
    compute = serpy.BoolField()
    contra_address_id = serpy.Field()
    credit_limit = serpy.StrField(required=False)
    customer = serpy.BoolField()
    note = serpy.Field(required=False)
    reference = serpy.Field()
    service_centre = serpy.BoolField()
    supplier = serpy.BoolField()
    territory = TerritorySerializer(required=False)
    uri = serpy.Field(attr='get_absolute_url', call=True)
    warrantor = serpy.BoolField()

    # Backwards Compatibility
    old_address_id = serpy.Field(attr='address_id', label='idAddress')
    old_contra_address_id = serpy.Field(attr='contra_address_id', label='idAddressContra')
    old_territory_id = serpy.Field(attr='territory_id', label='idTerritory')
