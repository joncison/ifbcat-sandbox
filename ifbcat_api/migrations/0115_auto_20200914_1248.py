# Generated by Django 3.0.7 on 2020-09-14 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ifbcat_api', '0114_auto_20200914_1232'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='organisedByBioinformaticsTeams',
            field=models.ManyToManyField(blank=True, help_text='A BioInformaticsTeam that is organizing the event.', related_name='organized_events_as_bioinfo', to='ifbcat_api.BioinformaticsTeam'),
        ),
        migrations.AddField(
            model_name='event',
            name='organisedByOrganisations',
            field=models.ManyToManyField(blank=True, help_text='An organisation that is organizing the event.', related_name='organized_events', to='ifbcat_api.Organisation'),
        ),
        migrations.AddField(
            model_name='event',
            name='organisedByTeams',
            field=models.ManyToManyField(blank=True, help_text='A Team that is organizing the event.', related_name='organized_events', to='ifbcat_api.Team'),
        ),
    ]