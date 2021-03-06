# Generated by Django 2.2.11 on 2020-10-09 15:07

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0013_email_confirmation'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(null=True)),
                ('extra', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('minio_access_key', models.CharField(max_length=100, null=True)),
                ('minio_secret_key', models.CharField(max_length=100, null=True)),
                ('minio_url', models.CharField(max_length=240, null=True)),
            ],
            options={
                'db_table': 'app_settings',
            },
        ),
    ]
