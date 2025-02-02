# Generated by Django 4.2.13 on 2025-01-06 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auto', '0003_auto_duong_chat_1_auto_duong_chat_2_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auto',
            name='duong_chat_3',
        ),
        migrations.RemoveField(
            model_name='auto',
            name='ph_pin',
        ),
        migrations.AddField(
            model_name='auto',
            name='vanph_max_pin',
            field=models.CharField(default='V1', help_text='PIN value from V0 to V50', max_length=3),
        ),
        migrations.AddField(
            model_name='auto',
            name='vanph_min_pin',
            field=models.CharField(default='V2', help_text='PIN value from V0 to V50', max_length=3),
        ),
        migrations.AlterField(
            model_name='auto',
            name='duong_chat_1',
            field=models.CharField(default='V3', help_text='PIN for dưỡng chất 1 (V0 to V50)', max_length=3),
        ),
        migrations.AlterField(
            model_name='auto',
            name='duong_chat_2',
            field=models.CharField(default='V4', help_text='PIN for dưỡng chất 2 (V0 to V50)', max_length=3),
        ),
    ]
