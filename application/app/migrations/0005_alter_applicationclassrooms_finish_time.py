# Generated by Django 4.2.4 on 2024-10-01 21:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_applications_event_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationclassrooms',
            name='finish_time',
            field=models.TimeField(blank=True, default=datetime.time(19, 0), null=True),
        ),
    ]
