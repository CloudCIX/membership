# libs
import serpy


__all__ = [
    'CurrencySerializer',
]


class CurrencySerializer(serpy.Serializer):
    """
    id:
        description: The id of the Currency
        type: integer
    name:
        description: The name of the Currency
        type: string
    symbol:
        description: The three letter name for the Currency used in CloudCIX
        type: string
    uri:
        description: The absolute URL of the Currency that can be used to perform `Read` operations on it
        type: string
    """
    id = serpy.Field()
    name = serpy.Field()
    symbol = serpy.Field()
    uri = serpy.Field(attr='get_absolute_url', call=True)

    # Backwards Compatibility
    old_id = serpy.Field(attr='pk', label='idCurrency')
