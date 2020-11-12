# Generated by Django 3.0.7 on 2020-11-09 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ifbcat_api', '0133_auto_20201105_1458'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text="Name of the certification, e.g. 'Label IBiSA'.", max_length=255, unique=True)),
                ('description', models.TextField(help_text='Short description of the certification.')),
                ('homepage', models.URLField(help_text='Homepage of the certification.', max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Certifications',
            },
        ),
        migrations.RemoveField(
            model_name='team',
            name='certification',
        ),
        migrations.AddField(
            model_name='team',
            name='certifications',
            field=models.ManyToManyField(blank=True, help_text='Certification(s) possessed by the team.', related_name='teamsCertifications', to='ifbcat_api.Certification'),
        ),
    ]