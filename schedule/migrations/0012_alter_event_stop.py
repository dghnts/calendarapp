# Generated by Django 4.2.5 on 2023-10-28 05:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0011_alter_event_stop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='stop',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2026, 7, 24, 5, 37, 24, 78995, tzinfo=datetime.timezone.utc), null=True, verbose_name='繰り返し終了日'),
        ),
    ]