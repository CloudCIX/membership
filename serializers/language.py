# libs
import serpy


__all__ = [
    'LanguageSerializer',
]


class LanguageSerializer(serpy.Serializer):
    """
    code:
        description: The ISO 639-1 code representing the Language
        type: string
    english_name:
        description: The name of the language in English
        type: string
    id:
        description: The id of the Language
        type: integer
    native_name:
        description: The name of the Language in that Language
        type: string
    uri:
        description: The absolute URL of the Language that can be used to perform `Read` operations on it
        type: string
    """
    code = serpy.Field()
    english_name = serpy.Field()
    id = serpy.Field()
    native_name = serpy.Field()
    uri = serpy.Field(attr='get_absolute_url', call=True)

    # Backwards Compatibility
    old_code = serpy.Field(attr='code', label='languageCode')
    old_english_name = serpy.Field(attr='english_name', label='name')
    old_id = serpy.Field(attr='pk', label='idLanguage')
    old_native_name = serpy.Field(attr='native_name', label='nativeName')
