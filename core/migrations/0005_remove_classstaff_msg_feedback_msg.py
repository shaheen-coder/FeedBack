# Generated by Django 5.1.3 on 2024-12-24 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_classstaff_msg'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classstaff',
            name='msg',
        ),
        migrations.AddField(
            model_name='feedback',
            name='msg',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
