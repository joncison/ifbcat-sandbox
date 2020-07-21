# Generated by Django 3.0 on 2020-07-21 17:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ifbcatsandbox_api', '0054_event_contactid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='name',
            field=models.CharField(help_text='Name of the organisation.', max_length=255, unique=True, validators=[django.core.validators.RegexValidator('^[a-zA-Z0-9 \\-_~]+$', 'Should only contains char such as ^[a-zA-Z0-9\\-_~]')]),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the project.', max_length=255)),
                ('homepage', models.URLField(blank=True, help_text='Homepage of the project.', max_length=255, null=True)),
                ('description', models.TextField(help_text='Description of the project.')),
                ('communities', models.ManyToManyField(blank=True, help_text='Community for which the project is relevant.', related_name='projects', to='ifbcatsandbox_api.Community')),
                ('elixirPlatforms', models.ManyToManyField(blank=True, help_text='ELIXIR Platform to which the project is relevant.', related_name='projects', to='ifbcatsandbox_api.ElixirPlatform')),
                ('fundedBy', models.ManyToManyField(blank=True, help_text='Organisation that funds the project.', related_name='projectsFunders', to='ifbcatsandbox_api.Organisation')),
                ('hostedBy', models.ManyToManyField(blank=True, help_text='Organisation that hosts the project.', related_name='projectsHosts', to='ifbcatsandbox_api.Organisation')),
                ('topics', models.ManyToManyField(help_text='URI of EDAM Topic term describing the expertise of the project.', related_name='projects', to='ifbcatsandbox_api.EventTopic')),
            ],
        ),
    ]