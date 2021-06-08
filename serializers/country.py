# libs
import serpy


__all__ = [
    'CountrySerializer',
]


class CountrySerializer(serpy.Serializer):
    """
    alpha_2_code:
        description: The ISO 3166-1 alpha-2 code for the Country
        type: string
    alpha_3_code:
        description: The ISO 3166-1 alpha-3 code for the Country
        type: string
    english_name:
        description: The name of the Country in English
        type: string
    id:
        description: The id of the Country record
        type: integer
    phone_prefix:
        description: The phone prefix used in the Country
        type: string
    primary_level_name:
        description: The name of the Country's primary level
        type: string
    uri:
        description: The absolute URL of the Country that can be used to perform `Read` operations on it
        type: string
    """
    alpha_2_code = serpy.Field()
    alpha_3_code = serpy.Field()
    english_name = serpy.Field()
    id = serpy.Field()
    phone_prefix = serpy.Field(required=False)
    primary_level_name = serpy.Field(required=False)
    uri = serpy.Field(attr='get_absolute_url', call=True)

    # Backwards Compatibility
    old_alpha_2_code = serpy.Field(attr='alpha_2_code', label='a2Code')
    old_alpha_3_code = serpy.Field(attr='alpha_3_code', label='a3Code')
    old_english_name = serpy.Field(attr='english_name', label='country')
    old_id = serpy.Field(attr='pk', label='idCountry')
    old_primary_level_name = serpy.Field(attr='primary_level_name', label='primaryLevelName')
