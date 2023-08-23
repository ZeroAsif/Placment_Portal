# Generated by Django 4.2.4 on 2023-08-21 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_remove_jobposting_application_checkbox_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobposting',
            name='salary_range_max',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='jobposting',
            name='salary_range_min',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
