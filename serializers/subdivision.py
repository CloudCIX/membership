# libs
import serpy
# local
from membership.serializers.country import CountrySerializer


__all__ = [
    'SubdivisionSerializer',
]


class SubdivisionSerializer(serpy.Serializer):
    """
    alpha_code:
        description: ISO 3166-2 code for the Subdivision
        type: string
    country:
        $ref: '#/components/schemas/Country'
    english_name:
        description: The name of the Subdivision in English
        type: string
    id:
        description: The id of the Subdivision
        type: integer
    uri:
        description: The absolute URL of the Subdivision that can be used to perform `Read` operations on it
        type: string
    """
    alpha_code = serpy.Field(required=False)
    country = CountrySerializer()
    english_name = serpy.Field(required=False)
    id = serpy.Field()
    uri = serpy.Field(attr='get_absolute_url', call=True)

    # Backwards Compatibility
    old_alpha_code = serpy.Field(attr='alpha_code', label='a2Code')
    old_country_id = serpy.Field(attr='country_id', label='idCountry')
    old_english_name = serpy.Field(attr='english_name', label='name')
    old_id = serpy.Field(attr='pk', label='idSubdivision')
