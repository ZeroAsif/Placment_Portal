# Generated by Django 4.2.4 on 2023-08-20 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_jobposting_application_checkbox'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobposting',
            name='application_checkbox',
            field=models.BooleanField(choices=[('on', 'hiring'), ('off', 'hiring_closed')], default=True),
        ),
    ]