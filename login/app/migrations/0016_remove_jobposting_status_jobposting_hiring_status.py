# Generated by Django 4.2.4 on 2023-08-26 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_remove_jobposting_hiring_status_jobposting_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobposting',
            name='status',
        ),
        migrations.AddField(
            model_name='jobposting',
            name='hiring_status',
            field=models.CharField(choices=[('hiring', 'Hiring'), ('hiring_closed', 'Hiring Closed')], default='hiring', max_length=20),
        ),
    ]