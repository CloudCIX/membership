# Generated by Django 2.2.13 on 2020-06-29 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0015_integritytest'),
    ]

    operations = [
        migrations.AddField(
            model_name='addresslink',
            name='extra_reference1',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='addresslink',
            name='extra_reference2',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='addresslink',
            name='extra_reference3',
            field=models.TextField(null=True),
        ),
    ]