# Generated by Django 4.2.4 on 2023-09-03 11:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0021_jobposting_selected'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobposting',
            name='selected',
        ),
        migrations.CreateModel(
            name='SelectedStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('selected', models.BooleanField(default=False)),
                ('company_name', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.jobposting')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
