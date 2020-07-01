# Generated by Django 3.0 on 2020-07-01 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ifbcatsandbox_api', '0011_auto_20200701_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='maxParticipants',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(help_text='Email address of a person (IFB catalogue user).', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='firstname',
            field=models.CharField(help_text='First (or given) name of a person (IFB catalogue user).', max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='homepage',
            field=models.URLField(blank=True, help_text='Homepage of a person (IFB catalogue user).', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Whether a user account is active.'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='Whether a user is a superuser.'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='lastname',
            field=models.CharField(help_text='Last (or family) name of a person (IFB catalogue user).', max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='orcidid',
            field=models.CharField(blank=True, help_text='ORCID ID of a person (IFB catalogue user).', max_length=255, null=True, unique=True),
        ),
    ]
