# Generated by Django 5.0.7 on 2024-09-17 06:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('regno', models.BigIntegerField()),
                ('dept', models.CharField(choices=[('CSE', 'Computer Science and Engineering'), ('I.T', 'Tnformation Technology '), ('ICE', 'Instrumentation and Controls Engineering'), ('EEE', 'Electrical and Electronics Engineering')], max_length=50)),
                ('section', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('subject_code', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('dept', models.CharField(max_length=20)),
                ('gender', models.BooleanField(choices=[(1, 'male'), (0, 'female')])),
                ('hclass', models.CharField(max_length=1)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.subject')),
            ],
        ),
        migrations.CreateModel(
            name='FeedBack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat1', models.SmallIntegerField()),
                ('cat2', models.SmallIntegerField()),
                ('cat3', models.SmallIntegerField()),
                ('cat4', models.SmallIntegerField()),
                ('cat5', models.SmallIntegerField()),
                ('avg_cat', models.FloatField(editable=False)),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.staff')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.subject')),
            ],
        ),
    ]
