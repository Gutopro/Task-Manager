# Generated by Django 5.0.6 on 2024-05-19 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]