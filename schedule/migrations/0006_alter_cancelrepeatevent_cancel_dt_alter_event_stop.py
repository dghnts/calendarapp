# Generated by Django 4.2.5 on 2023-10-16 01:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0005_alter_event_stop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cancelrepeatevent',
            name='cancel_dt',
            field=models.DateTimeField(verbose_name='キャンセル日時'),
        ),
        migrations.AlterField(
            model_name='event',
            name='stop',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2026, 7, 12, 1, 4, 16, 740290, tzinfo=datetime.timezone.utc), null=True, verbose_name='繰り返し終了日'),
        ),
    ]