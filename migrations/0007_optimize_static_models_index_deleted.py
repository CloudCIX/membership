from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0006_addresslink_credit_limit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='currency',
            name='created',
        ),
        migrations.RemoveField(
            model_name='currency',
            name='deleted',
        ),
        migrations.RemoveField(
            model_name='currency',
            name='extra',
        ),
        migrations.RemoveField(
            model_name='currency',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='language',
            name='created',
        ),
        migrations.RemoveField(
            model_name='language',
            name='deleted',
        ),
        migrations.RemoveField(
            model_name='language',
            name='extra',
        ),
        migrations.RemoveField(
            model_name='language',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='subdivision',
            name='created',
        ),
        migrations.RemoveField(
            model_name='subdivision',
            name='deleted',
        ),
        migrations.RemoveField(
            model_name='subdivision',
            name='extra',
        ),
        migrations.RemoveField(
            model_name='subdivision',
            name='updated',
        ),
        migrations.AddIndex(
            model_name='address',
            index=models.Index(fields=['deleted'], name='address_deleted'),
        ),
        migrations.AddIndex(
            model_name='department',
            index=models.Index(fields=['deleted'], name='department_deleted'),
        ),
        migrations.AddIndex(
            model_name='member',
            index=models.Index(fields=['deleted'], name='member_deleted'),
        ),
        migrations.AddIndex(
            model_name='memberlink',
            index=models.Index(fields=['id'], name='member_link_id'),
        ),
        migrations.AddIndex(
            model_name='memberlink',
            index=models.Index(fields=['deleted'], name='member_link_deleted'),
        ),
        migrations.AddIndex(
            model_name='profile',
            index=models.Index(fields=['deleted'], name='profile_deleted'),
        ),
        migrations.AddIndex(
            model_name='team',
            index=models.Index(fields=['deleted'], name='team_deleted'),
        ),
        migrations.AddIndex(
            model_name='territory',
            index=models.Index(fields=['deleted'], name='territory_deleted'),
        ),
        migrations.AddIndex(
            model_name='transactiontype',
            index=models.Index(fields=['deleted'], name='transaction_type_deleted'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['administrator'], name='user_administrator'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['deleted'], name='user_deleted'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['first_name'], name='user_first_name'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['global_active'], name='user_global_active'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['global_user'], name='user_global_user'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['job_title'], name='user_job_title'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['last_login'], name='user_last_login'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['start_date'], name='user_start_date'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['surname'], name='user_surname'),
        ),
    ]
