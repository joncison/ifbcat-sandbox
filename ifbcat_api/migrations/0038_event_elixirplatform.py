# Generated by Django 3.0 on 2020-07-20 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ifbcat_api', '0037_auto_20200720_1905'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='elixirPlatform',
            field=models.ManyToManyField(help_text='ELIXIR Platform to which the event is relevant.', related_name='events', to='ifbcat_api.ElixirPlatform'),
        ),
    ]