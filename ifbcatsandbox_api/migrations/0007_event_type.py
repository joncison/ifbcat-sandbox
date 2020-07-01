# Generated by Django 3.0 on 2020-07-01 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ifbcatsandbox_api', '0006_auto_20200629_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='type',
            field=models.CharField(blank=True, choices=[('WO', 'Workshop'), ('TR', 'Training course'), ('ME', 'Meeting'), ('CO', 'Conference')], max_length=2),
        ),
    ]
