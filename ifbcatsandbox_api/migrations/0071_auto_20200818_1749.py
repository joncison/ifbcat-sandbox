# Generated by Django 3.0 on 2020-08-18 17:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ifbcatsandbox_api', '0070_auto_20200818_1609'),
    ]

    operations = [
        migrations.CreateModel(
            name='BioinformaticsTeam',
            fields=[
                ('team_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ifbcatsandbox_api.Team')),
                ('orgid', models.CharField(help_text='Organisation ID (GRID or ROR ID) of the team.', max_length=255, unique=True)),
                ('unitId', models.CharField(blank=True, help_text='Unit ID (unique identifier of research or service unit) that the Bioinformatics Team belongs to.', max_length=255)),
                ('address', models.TextField(blank=True, help_text='Postal address of the bioinformatics team.')),
                ('ifbMembership', models.CharField(choices=[('IFB platform', 'IFB platform'), ('IFB-associated team', 'IFB-associated team'), ('Not a member', 'Not a member')], help_text='Type of membership the bioinformatics team has to IFB.', max_length=255)),
                ('certification', models.CharField(blank=True, choices=[('Certificate 1', 'Certificate 1')], help_text='Certification (e.g. ISO) of the bioinformatics team.', max_length=255)),
                ('affiliatedWith', models.ManyToManyField(blank=True, help_text='Organisation(s) to which the bioinformatics team is affiliated.', related_name='bioinformaticsTeamsAffiliatedWith', to='ifbcatsandbox_api.Organisation')),
                ('communities', models.ManyToManyField(blank=True, help_text='Communities in which the bioinformatics team is involved.', related_name='bioinformaticsTeams', to='ifbcatsandbox_api.Community')),
                ('fields', models.ManyToManyField(blank=True, help_text='A broad field that the bioinformatics team serves.', related_name='bioinformaticsTeams', to='ifbcatsandbox_api.OrganisationField')),
                ('fundedBy', models.ManyToManyField(help_text='Organisation(s) that funds the bioinformatics team.', related_name='bioinformaticsTeamsFundedBy', to='ifbcatsandbox_api.Organisation')),
                ('keywords', models.ManyToManyField(blank=True, help_text='A keyword (beyond EDAM ontology scope) describing the bioinformatics team.', related_name='bioinformaticsTeams', to='ifbcatsandbox_api.EventKeyword')),
                ('platforms', models.ManyToManyField(blank=True, help_text='ELIXIR Platform(s) in which the bioinformatics team is involved.', related_name='bioinformaticsTeams', to='ifbcatsandbox_api.ElixirPlatform')),
                ('projects', models.ManyToManyField(blank=True, help_text='Project(s) that the bioinformatics team is involved with, supports or hosts.', related_name='bioinformaticsTeams', to='ifbcatsandbox_api.Project')),
            ],
            bases=('ifbcatsandbox_api.team',),
        ),
        migrations.CreateModel(
            name='Doi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doi', models.CharField(help_text='A digital object identifier (DOI) of a publication or training material.', max_length=255, unique=True)),
            ],
        ),
        migrations.DeleteModel(
            name='BioiformaticsTeam',
        ),
        migrations.AddField(
            model_name='bioinformaticsteam',
            name='publications',
            field=models.ManyToManyField(blank=True, help_text='Publication(s) that describe the team.', related_name='bioinformaticsTeams', to='ifbcatsandbox_api.Doi'),
        ),
        migrations.AddField(
            model_name='bioinformaticsteam',
            name='topics',
            field=models.ManyToManyField(blank=True, help_text='URIs of EDAM Topic terms describing the bioinformatics team.', related_name='bioinformaticsTeams', to='ifbcatsandbox_api.EventTopic'),
        ),
    ]
