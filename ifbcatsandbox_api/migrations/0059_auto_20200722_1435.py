# Generated by Django 3.0 on 2020-07-22 14:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ifbcatsandbox_api', '0058_create_organisation_field'),
    ]

    operations = [
        migrations.CreateModel(
            name='AudienceRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audienceRole', models.CharField(choices=[('Researchers', 'Researchers'), ('Life scientists', 'Life scientists'), ('Computer scientists', 'Computer scientists'), ('Biologists', 'Biologists'), ('Bioinformaticians', 'Bioinformaticians'), ('Programmers', 'Programmers'), ('Curators', 'Curators'), ('Managers', 'Managers'), ('All', 'All')], help_text='The professional roles of the expected audience of the training event or material.', max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='AudienceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audienceType', models.CharField(choices=[('Undergraduate', 'Undergraduate'), ('Graduate', 'Graduate'), ('Professional (initial)', 'Professional (initial)'), ('Professional (continued)', 'Professional (continued)')], help_text='The education or professional level of the expected audience of the training event or material.', max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the resource.', max_length=255)),
                ('description', models.TextField(help_text='A short description of the resource.')),
                ('communities', models.ManyToManyField(blank=True, help_text='Community which uses the resource.', related_name='resources', to='ifbcatsandbox_api.Community')),
                ('elixirPlatforms', models.ManyToManyField(blank=True, help_text='ELIXIR Platform which uses the resource.', related_name='resources', to='ifbcatsandbox_api.ElixirPlatform')),
                ('user_profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='eventcost',
            name='cost',
            field=models.CharField(help_text="Monetary cost to attend the event, e.g. 'Free to academics'.", max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='organisationfield',
            name='field',
            field=models.CharField(help_text='A broad field that the organisation serves.', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='homepage',
            field=models.URLField(default='https://test.com', help_text='Homepage of the project.', max_length=255),
        ),
        migrations.CreateModel(
            name='TrainingMaterial',
            fields=[
                ('resource_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ifbcatsandbox_api.Resource')),
                ('doi', models.CharField(blank=True, help_text='Unique identier (DOI) of the training material, e.g. a Zenodo DOI.', max_length=255, null=True, unique=True)),
                ('fileLocation', models.URLField(help_text='A link to where the training material can be downloaded or accessed.', max_length=255)),
                ('fileName', models.CharField(help_text='The name of a downloadable file containing the training material.', max_length=255)),
                ('difficultyLevel', models.CharField(blank=True, choices=[('Novice', 'Novice'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')], help_text='The required experience and skills of the expected audience of the training material.', max_length=255)),
                ('dateCreation', models.DateField(help_text='Date when the training material was created.')),
                ('dateUpdate', models.DateField(help_text='Date when the training material was updated.')),
                ('license', models.CharField(blank=True, choices=[('Test license 1', 'Test license 1'), ('Test license 2', 'Test license 2')], help_text='License under which the training material is made available.', max_length=255)),
                ('audienceRoles', models.ManyToManyField(blank=True, help_text='The professional roles of the expected audience of the training material.', related_name='trainingMaterials', to='ifbcatsandbox_api.AudienceRole')),
                ('audienceTypes', models.ManyToManyField(blank=True, help_text='The education or professional level of the expected audience of the training material.', related_name='trainingMaterials', to='ifbcatsandbox_api.AudienceType')),
                ('keywords', models.ManyToManyField(blank=True, help_text='A keyword (beyond EDAM ontology scope) describing the training material.', related_name='trainingMaterials', to='ifbcatsandbox_api.EventKeyword')),
                ('topics', models.ManyToManyField(blank=True, help_text='URI of EDAM Topic term describing the scope of the training material.', related_name='trainingMaterials', to='ifbcatsandbox_api.EventTopic')),
            ],
            bases=('ifbcatsandbox_api.resource',),
        ),
    ]
