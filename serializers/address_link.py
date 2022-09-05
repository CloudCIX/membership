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
    cloud_builder:
        description: A flag stating if the Contra Address is a Builder of Cloud resources
        type: boolean
    cloud_customer:
        description: A flag stating if the Contra Address can build cloud resources in the Address' region
        type: boolean
    cloud_distributor:
        description: A flag stating if the Contra Address is set up to sell Cloud resources built by a builder.
        type: boolean
    cloud_export_markup:
        type: string
        format: decimal
        description: |
            Export Markup CloudCIX assigns to Cloud Distributors for virtual infrastructure built where the builder is
            not the distributor. Example of an export markup would be for duty on exports from Ireland to distributors
            business country and CloudCIX profit margin.
    cloud_import_markup:
        type: string
        format: decimal
        description: |
            Import Markup CloudCIX assigns to Cloud Builders for virtual infrastructure built where the distributor is
            not the builder. Example of an import markup would be for duty on imports to Ireland.
    cloud_seller:
        description: A flag stating if the Contra Address is set up to sell Resources from a Distributor to a Customer
        type: boolean
    cloud_seller_markup:
        type: string
        format: decimal
        description: |
            The markup the Cloud Seller to each of it's customers for virtual infrastructure built in regions the
            seller (distributor) is not the builder.
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
    extra:
        description: A dictionary of key, value pairs containing any extra data about the Link
        type: string
    extra_reference1:
        description: An extra bit of reference text about the address link
        type: string
    extra_reference2:
        description: An extra bit of reference text about the address link
        type: string
    extra_reference3:
        description: An extra bit of reference text about the address link
        type: string
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
    cloud_builder = serpy.BoolField()
    cloud_customer = serpy.BoolField()
    cloud_distributor = serpy.BoolField()
    cloud_export_markup = serpy.StrField()
    cloud_import_markup = serpy.StrField()
    cloud_seller = serpy.BoolField()
    cloud_seller_markup = serpy.StrField()
    contra_address_id = serpy.Field()
    credit_limit = serpy.StrField(required=False)
    customer = serpy.BoolField()
    extra = serpy.Field()
    extra_reference1 = serpy.Field()
    extra_reference2 = serpy.Field()
    extra_reference3 = serpy.Field()
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
