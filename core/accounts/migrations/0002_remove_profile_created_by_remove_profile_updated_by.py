# Generated by Django 5.0.6 on 2024-05-28 10:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='updated_by',
        ),
    ]
