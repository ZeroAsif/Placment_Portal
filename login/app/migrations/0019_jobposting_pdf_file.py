# Generated by Django 4.2.4 on 2023-08-27 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_alter_jobposting_hiring_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobposting',
            name='pdf_file',
            field=models.FileField(default=None, upload_to='job_pdfs/'),
            preserve_default=False,
        ),
    ]