# libs
import serpy
# local
from membership.serializers.address_link import AddressLinkSerializer
from membership.serializers.country import CountrySerializer
from membership.serializers.currency import CurrencySerializer
from membership.serializers.language import LanguageSerializer
from membership.serializers.member import MemberSerializer
from membership.serializers.subdivision import SubdivisionSerializer


__all__ = [
    'AddressSerializer',
]


class AddressSerializer(serpy.Serializer):
    """
    address1:
        description: The first line of the geographic address of the Address
        type: string
    address2:
        description: The second line of the geographic address of the Address
        type: string
    address3:
        description: The third line of the geographic address of the Address
        type: string
    billing_address_id:
        description: The id of the Address that receives bills for the Address
        type: integer
    city:
        description: The city in which the Address is located
        type: string
    cloud_region:
        description: A flag stating if this Address is a Cloud Region for IaaS
        type: boolean
    country:
       $ref: '#/components/schemas/Country'
    currency:
        $ref: '#/components/schemas/Currency'
    email:
        description: The email address of the Address
        type: string
    full_address:
        description: The full geographical address of the Address
        type: string
    gln:
        description: The Global Location Number of the Address
        type: string
    id:
        description: The id of the Address
        type: integer
    language:
        $ref: '#/components/schemas/Language'
    link:
        $ref: '#/components/schemas/AddressLink'
    linked:
        description: A flag stating whether the requesting User's Address is linked to this one
        type: boolean
    member:
        $ref: '#/components/schemas/Member'
    name:
        description: The name of the Address
        type: string
    phones:
        description: An array of named phone numbers used by this Address
        type: array
        items:
            type: object
            properties:
                name:
                    type: string
                number:
                    type: string
    postcode:
        description: The postcode of the geographical address of the Address
        type: string
    subdivision:
        $ref: '#/components/schemas/Subdivision'
    uri:
        description: The absolute URL of the Address that can be used to perform `Read` and `Update` operations on it
        type: string
    vat_number:
        description: The vat number of the Address
        type: string
    website:
        description: The website of the Address
        type: string
    """
    address1 = serpy.Field()
    address2 = serpy.Field()
    address3 = serpy.Field()
    billing_address_id = serpy.Field()
    city = serpy.Field()
    cloud_region = serpy.BoolField()
    country = CountrySerializer()
    currency = CurrencySerializer()
    email = serpy.Field()
    full_address = serpy.Field()
    gln = serpy.Field(required=False)
    id = serpy.Field()
    language = LanguageSerializer()
    link = AddressLinkSerializer(required=False)
    linked = serpy.Field(required=False)
    member = MemberSerializer()
    name = serpy.Field()
    phones = serpy.Field()
    postcode = serpy.Field()
    subdivision = SubdivisionSerializer(required=False)
    uri = serpy.Field(attr='get_absolute_url', call=True)
    vat_number = serpy.Field()
    website = serpy.Field()

    # Backwards Compatibility
    old_billing_address_id = serpy.Field(attr='billing_address_id', label='idAddressBilling')
    old_country_id = serpy.Field(attr='country_id', label='idCountry')
    old_currency_id = serpy.Field(attr='currency_id', label='idCurrency')
    old_full_address = serpy.Field(attr='full_address', label='fullAddress')
    old_id = serpy.Field(attr='id', label='idAddress')
    old_language_id = serpy.Field(attr='language_id', label='idLanguage')
    old_member_id = serpy.Field(attr='member_id', label='idMember')
    old_name = serpy.Field(attr='name', label='companyName')
    old_subdivision_id = serpy.Field(attr='subdivision_id', label='idSubdivision')
    old_vat_number = serpy.Field(attr='vat_number', label='vatNumber')
