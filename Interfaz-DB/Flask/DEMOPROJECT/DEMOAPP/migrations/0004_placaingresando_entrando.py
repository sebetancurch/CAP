# Generated by Django 3.2 on 2021-08-24 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DEMOAPP', '0003_auto_20210823_2109'),
    ]

    operations = [
        migrations.AddField(
            model_name='placaingresando',
            name='entrando',
            field=models.BooleanField(default=True),
        ),
    ]
