# Generated by Django 3.0 on 2020-08-27 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ifbcatsandbox_api', '0088_auto_20200826_1740'),
    ]

    operations = [
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field', models.CharField(help_text='A broad field that the organisation or bioinformatics serves.', max_length=255, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='bioinformaticsteam',
            name='fields',
            field=models.ManyToManyField(blank=True, help_text='A broad field that the bioinformatics team serves.', related_name='bioinformaticsTeams', to='ifbcatsandbox_api.Field'),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='fields',
            field=models.ManyToManyField(blank=True, help_text='A broad field that the organisation serves.', related_name='organisations', to='ifbcatsandbox_api.Field'),
        ),
    ]
