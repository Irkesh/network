# Generated by Django 3.0.3 on 2023-09-01 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0005_auto_20230901_1532'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='friends',
            field=models.ManyToManyField(blank=True, to='social.AppUser'),
        ),
    ]
