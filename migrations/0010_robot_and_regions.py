# Generated by Django 2.2.11 on 2020-06-24 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0009_otp_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='cloud_region',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='robot',
            field=models.BooleanField(default=False),
        ),
        migrations.AddIndex(
            model_name='address',
            index=models.Index(fields=['cloud_region'], name='address_cloud_region'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['robot'], name='user_robot'),
        ),
    ]
