# libs
import serpy


__all__ = [
    'TransactionTypeSerializer',
]


class TransactionTypeSerializer(serpy.Serializer):
    """
    id:
        description: The id of the Transaction Type
        type: integer
    name:
        description: The name of the Transaction Type
        type: string
    uri:
        description: The absolute URL of the Transaction Type that can be used to perform `Read` operations on it
        type: string
    """
    id = serpy.Field()
    name = serpy.Field(required=False)
    uri = serpy.Field(attr='get_absolute_url', call=True)

    # Backwards Compatibility
    old_id = serpy.Field(attr='pk', label='idTransactionType')
