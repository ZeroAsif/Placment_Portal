# Generated by Django 4.2.4 on 2023-09-05 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_alter_selectedstudent_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selectedstudent',
            name='message',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
    ]
