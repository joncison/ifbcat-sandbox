# Generated by Django 3.0 on 2020-09-03 10:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ifbcat_api', '0101_auto_20200902_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='accessibility',
            field=models.CharField(choices=[('Public', 'Public'), ('Private', 'Private')], help_text='Whether the event is public or private.', max_length=255),
        ),
        migrations.AlterField(
            model_name='keyword',
            name='keyword',
            field=models.CharField(help_text='A keyword (beyond EDAM ontology scope).', max_length=255, unique=True, validators=[django.core.validators.RegexValidator('^[a-zA-Z0-9 \\-_~]+$', 'Should only contains char such as ^[a-zA-Z0-9\\-_~]')]),
        ),
    ]
