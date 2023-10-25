# Generated by Django 4.2.5 on 2023-10-25 01:43

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schedule', '0007_alter_event_stop_schedulenotified'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ScheduleNotified',
            new_name='EventNotified',
        ),
        migrations.AlterField(
            model_name='event',
            name='stop',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2026, 7, 21, 1, 43, 17, 521025, tzinfo=datetime.timezone.utc), null=True, verbose_name='繰り返し終了日'),
        ),
    ]
