# Generated by Django 3.1.7 on 2021-03-06 13:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loan',
            name='is_rejected',
        ),
    ]