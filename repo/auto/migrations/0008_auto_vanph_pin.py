# Generated by Django 4.2.13 on 2025-01-06 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auto', '0007_alter_auto_van_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='auto',
            name='vanph_pin',
            field=models.CharField(default='V9', help_text='PIN value from V0 to V50', max_length=3),
        ),
    ]
