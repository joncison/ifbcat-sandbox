# Generated by Django 2.2 on 2020-06-27 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ifbcatsandbox_api', '0003_auto_20200627_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='orcidid',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
