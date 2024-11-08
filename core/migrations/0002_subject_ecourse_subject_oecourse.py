# Generated by Django 5.1.2 on 2024-11-07 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='ecourse',
            field=models.BooleanField(default=False, help_text='elective course'),
        ),
        migrations.AddField(
            model_name='subject',
            name='oecourse',
            field=models.BooleanField(default=False, help_text='open elective course'),
        ),
    ]
