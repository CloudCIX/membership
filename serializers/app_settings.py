# libs
import serpy


class AppSettingsSerializer(serpy.Serializer):
    """
    created:
        description: The date that the App Settings entry was created.
        type: string
    id:
        description: The ID of the App Settings record.
        type: integer
    minio_access_key:
        description: Access key is like user ID that uniquely identifies your MinIO account.
        type: string
    minio_secret_key:
        description: TSecret key is the password to your MinIO account.
        type: string
    minio_url:
        description: The url for the MinIO instance for the COP.
        type: string
    updated:
        description: The date that the App Settings entry was last updated.
        type: string
    uri:
        description: |
            The absolute URL of the App Settings record that can be used to perform `Read`, `Update` and `Delete`.
        type: string
    """
    created = serpy.Field(attr='created.isoformat', call=True)
    id = serpy.Field()
    minio_access_key = serpy.Field()
    minio_secret_key = serpy.Field()
    minio_url = serpy.Field()
    updated = serpy.Field(attr='updated.isoformat', call=True)
    uri = serpy.Field(attr='get_absolute_url', call=True)
