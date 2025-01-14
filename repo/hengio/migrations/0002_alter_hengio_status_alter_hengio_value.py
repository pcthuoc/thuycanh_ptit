# Generated by Django 4.2.13 on 2025-01-06 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hengio', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hengio',
            name='status',
            field=models.IntegerField(choices=[(1, 'On'), (0, 'Off')], default=1, help_text='Value of the sensor'),
        ),
        migrations.AlterField(
            model_name='hengio',
            name='value',
            field=models.IntegerField(choices=[(1, 'On'), (0, 'Off')], default=1, help_text='Type'),
        ),
    ]
