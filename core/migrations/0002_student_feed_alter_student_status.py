# Generated by Django 5.1.3 on 2024-12-23 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='feed',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='status',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]
