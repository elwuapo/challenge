# Generated by Django 4.2.4 on 2023-08-28 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_rename_person_id_punch_person'),
    ]

    operations = [
        migrations.AddField(
            model_name='punch',
            name='punch_time',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]