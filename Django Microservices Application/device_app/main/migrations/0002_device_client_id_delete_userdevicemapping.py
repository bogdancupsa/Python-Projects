# Generated by Django 4.2 on 2023-11-13 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='client_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='UserDeviceMapping',
        ),
    ]
