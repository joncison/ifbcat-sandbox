# Generated by Django 3.0 on 2020-07-15 11:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ifbcatsandbox_api', '0019_auto_20200714_1407'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventPrerequisite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prerequisite', models.CharField(help_text="A skill which the audience should (ideally) possess to get the most out of the event, e.g. 'Python'.", max_length=255, unique=True)),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prerequisites', to='ifbcatsandbox_api.Event')),
                ('user_profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
