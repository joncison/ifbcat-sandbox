# Generated by Django 3.0 on 2020-08-25 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ifbcat_api', '0083_service'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trainingmaterial',
            name='license',
        ),
        migrations.AddField(
            model_name='trainingmaterial',
            name='license',
            field=models.CharField(blank=True, choices=[('License A', 'License A')], help_text='License under which the training material is made available.', max_length=255),
        ),
        migrations.DeleteModel(
            name='TrainingMaterialLicense',
        ),
    ]
