# Generated by Django 3.0 on 2020-08-13 12:04

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ifbcat_api', '0068_auto_20200813_1023'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingEvent',
            fields=[
                ('event_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ifbcat_api.Event')),
                ('difficultyLevel', models.CharField(blank=True, choices=[('Novice', 'Novice'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')], help_text='The required experience and skills of the expected audience of the training event.', max_length=255)),
                ('learningOutcomes', models.TextField(blank=True, help_text='Expected learning outcomes from the training event.')),
                ('hoursPresentations', models.PositiveSmallIntegerField(blank=True, help_text='Total time (hours) of presented training material.', null=True, validators=[django.core.validators.MinValueValidator(1)])),
                ('hoursHandsOn', models.PositiveSmallIntegerField(blank=True, help_text='Total time (hours) of hands-on / practical work.', null=True, validators=[django.core.validators.MinValueValidator(1)])),
                ('hoursTotal', models.PositiveSmallIntegerField(blank=True, help_text='Total time investment (hours) of the training event, including recommended prework.', null=True, validators=[django.core.validators.MinValueValidator(1)])),
                ('personalised', models.BooleanField(blank=True, help_text='Whether the training is tailored to the individual in some way (BYOD, personal tutoring etc.)', null=True)),
                ('audienceRoles', models.ManyToManyField(blank=True, help_text='The professional roles of the expected audience of the training event.', related_name='trainingEvents', to='ifbcat_api.AudienceRole')),
                ('audienceTypes', models.ManyToManyField(blank=True, help_text='The education or professional level of the expected audience of the training event.', related_name='trainingEvents', to='ifbcat_api.AudienceType')),
                ('computingFacilities', models.ManyToManyField(blank=True, help_text='Computing facilities that the training event uses.', related_name='trainingEvents', to='ifbcat_api.ComputingFacility')),
                ('trainers', models.ManyToManyField(blank=True, help_text='Details of people who are providing training at the training event.', related_name='trainingEvents', to='ifbcat_api.Trainer')),
                ('trainingMaterials', models.ManyToManyField(blank=True, help_text='Training material that the training event uses.', related_name='trainingEvents', to='ifbcat_api.TrainingMaterial')),
            ],
            bases=('ifbcat_api.event',),
        ),
        migrations.AddField(
            model_name='trainingeventmetrics',
            name='trainingEvent',
            field=models.ForeignKey(help_text='Training event to which the metrics are associated.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='metrics', to='ifbcat_api.TrainingEvent'),
        ),
    ]
