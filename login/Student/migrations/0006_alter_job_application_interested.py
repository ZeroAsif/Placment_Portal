# Generated by Django 4.2.4 on 2023-08-24 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0005_additionalskill_remove_languageskill_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job_application',
            name='interested',
            field=models.BooleanField(default=True),
        ),
    ]