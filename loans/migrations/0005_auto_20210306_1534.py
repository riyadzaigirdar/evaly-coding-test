# Generated by Django 3.1.7 on 2021-03-06 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0004_auto_20210306_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='is_accepted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='loan',
            name='is_returned',
            field=models.BooleanField(default=False),
        ),
    ]
