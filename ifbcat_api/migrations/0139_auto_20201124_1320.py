# Generated by Django 3.0.7 on 2020-11-24 13:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ifbcat_api', '0138_auto_20201123_1001'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tool',
            options={'ordering': ('name', 'biotoolsID')},
        ),
    ]
