# Generated by Django 4.2.13 on 2025-01-06 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auto', '0006_alter_auto_van_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auto',
            name='van_status',
            field=models.IntegerField(choices=[(1, 'Tu dong'), (2, 'thu cong')], help_text='Type'),
        ),
    ]
