# Generated by Django 4.2.5 on 2023-10-07 02:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='stop',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2026, 7, 3, 2, 50, 13, 48927, tzinfo=datetime.timezone.utc), null=True, verbose_name='繰り返し終了日'),
        ),
    ]
