# Generated by Django 4.2.4 on 2023-08-28 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_punch_punch_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='url',
            field=models.CharField(default='', max_length=256),
        ),
    ]
