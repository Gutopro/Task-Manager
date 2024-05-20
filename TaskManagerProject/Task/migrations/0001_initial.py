# Generated by Django 5.0.6 on 2024-05-20 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField(default='')),
                ('is_complete', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
