# Generated by Django 4.2.4 on 2023-08-26 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_jobposting_hiring_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobposting',
            name='hiring_status',
            field=models.CharField(choices=[('hiring', 'hiring_closed'), ('hiring_closed', 'Hiring ')], default='hiring', max_length=20),
        ),
    ]