# Generated by Django 3.0 on 2020-07-02 18:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ifbcatsandbox_api', '0016_eventkeyword'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventkeyword',
            name='event',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='keywords', to='ifbcatsandbox_api.Event'),
        ),
        migrations.AlterField(
            model_name='eventkeyword',
            name='keyword',
            field=models.CharField(help_text='A keyword (beyond EDAM ontology scope) describing the event.', max_length=255, unique=True),
        ),
    ]