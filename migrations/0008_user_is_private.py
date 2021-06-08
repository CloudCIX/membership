from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0007_optimize_static_models_index_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['is_private'], name='user_is_private'),
        ),
    ]
