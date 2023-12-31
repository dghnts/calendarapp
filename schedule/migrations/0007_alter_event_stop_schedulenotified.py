# Generated by Django 4.2.5 on 2023-10-23 00:19

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schedule', '0006_alter_cancelrepeatevent_cancel_dt_alter_event_stop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='stop',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2026, 7, 19, 0, 19, 42, 414303, tzinfo=datetime.timezone.utc), null=True, verbose_name='繰り返し終了日'),
        ),
        migrations.CreateModel(
            name='ScheduleNotified',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_dt', models.DateTimeField(verbose_name='スケジュールの日時')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.event', verbose_name='紐づくスケジュール')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='投稿者')),
            ],
        ),
    ]
