# Generated by Django 5.1.3 on 2024-12-24 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_remove_feedback_feed_remove_student_feed_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timescheduler',
            name='end_time',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='timescheduler',
            name='start_time',
            field=models.DateField(),
        ),
    ]
