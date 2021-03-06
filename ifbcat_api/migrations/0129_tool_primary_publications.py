# Generated by Django 3.0.7 on 2020-10-21 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ifbcat_api', '0128_auto_20201021_1439'),
    ]

    operations = [
        migrations.AddField(
            model_name='tool',
            name='primary_publications',
            field=models.ManyToManyField(blank=True, help_text='Publication(s) that describe the tool as a whole.', related_name='tools', to='ifbcat_api.Doi'),
        ),
    ]
