# Generated by Django 3.0 on 2020-07-22 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ifbcat_api', '0059_auto_20200722_1435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='homepage',
            field=models.URLField(help_text='Homepage of the project.', max_length=255),
        ),
    ]
