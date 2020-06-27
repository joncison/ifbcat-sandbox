# Generated by Django 2.2 on 2020-06-27 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ifbcatsandbox_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='homepage',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='orcidid',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
