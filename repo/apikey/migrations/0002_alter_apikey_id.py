# Generated by Django 4.2.13 on 2025-01-06 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apikey', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apikey',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
