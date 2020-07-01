# Generated by Django 3.0 on 2020-07-01 09:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ifbcatsandbox_api', '0008_event_user_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='maxParticipants',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
