# Generated by Django 2.1.5 on 2019-02-19 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0005_transaction_type_cleanup'),
    ]

    operations = [
        migrations.AddField(
            model_name='addresslink',
            name='credit_limit',
            field=models.DecimalField(null=True, max_digits=23, decimal_places=4),
        ),
    ]
