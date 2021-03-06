# Generated by Django 3.0 on 2020-07-21 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ifbcat_api', '0052_auto_20200721_1200'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganisationField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field', models.CharField(choices=[('Computer science', 'Computer science'), ('Biotechnology', 'Biotechnology'), ('Environmental science', 'Environmental science'), ('Agricultural science', 'Agricultural science'), ('Biomedical science', 'Biomedical science'), ('Biology', 'Biology')], help_text='A broad field that the organisation serves.', max_length=255, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='organisation',
            name='fields',
        ),
        migrations.AddField(
            model_name='organisation',
            name='fields',
            field=models.ManyToManyField(blank=True, help_text='A broad field that the organisation serves.', related_name='organisations', to='ifbcat_api.OrganisationField'),
        ),
    ]
