from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone

from django.utils.timezone import localtime

from config.settings import base


# カレンダーモデル
class Calendar(models.Model):
    # 作成したユーザー
    # 作成者のアカウントが消えたらカレンダーも同時に削除される
    user = models.ForeignKey(
        base.AUTH_USER_MODEL, verbose_name="作成者", on_delete=models.CASCADE
    )
    # 登録するカレンダーの名前
    name = models.CharField(verbose_name="カレンダー", max_length=100)

    # カレンダーを共有するユーザー名の指定
    # share = models.ManyToManyField(base.AUTH_USER_MODEL,verbose_name="公開範囲", related_name="share_calendar")

    permission = models.ManyToManyField(
        base.AUTH_USER_MODEL,
        verbose_name="公開範囲",
        through="CalendarPermission",
        related_name="calendar_permission",
        blank=True,
    )

    def __str__(self):
        return self.name


class CalendarPermission(models.Model):

    calendar = models.ForeignKey(
        Calendar, verbose_name="カレンダー", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        base.AUTH_USER_MODEL, verbose_name="対象ユーザー", on_delete=models.CASCADE
    )

    read = models.BooleanField(verbose_name="読み込み権限", default=False)
    write = models.BooleanField(verbose_name="書き込み権限", default=False)
    chat = models.BooleanField(verbose_name="チャット権限", default=False)

    def __str__(self):
        return self.calendar.name + "_" + self.user.username


# スケジュールモデル
class Event(models.Model):
    ###############################################################
    # field名はfullcalendarのプロパティに合わせる（propertyが存在しないものは最下部にまとまておく
    ###############################################################

    # スケジュールを登録するカレンダー
    # カレンダーが削除されると同時にスケジュールも削除される
    calendar = models.ForeignKey(
        Calendar, verbose_name="スケジュール", on_delete=models.CASCADE
    )

    # スケジュールの開始日
    # 日時はユーザーが指定するから，auto_now,auto_now_addはFalse
    start = models.DateTimeField(
        verbose_name="開始日時", auto_now=False, auto_now_add=False
    )

    # スケジュールの終了日
    # 日時はゆーザーが指定するから，auto_now,auto_now_addはFalse
    end = models.DateTimeField(
        verbose_name="開始日時", auto_now=False, auto_now_add=False
    )

    # スケジュールの内容（要約）
    title = models.CharField(max_length=200)

    ## 定期的に設定されるスケジュールに対する処理
    ## 繰り返し処理ではない場合，空欄で提出

    ## どのくらいのスパンで繰り返すか指定
    ## 繰り返しの初期値を7日間で設定
    # durationsfieldのdefault値はtimedelta型で指定する
    # repeat =  models.DurationField(verbose_name="繰り返し期間", default="", null=True, blank=True)
    # repeat =  models.DurationField(verbose_name="繰り返し期間", default=timedelta(days=7), null=True, blank=True)
    repeat = models.PositiveIntegerField(
        verbose_name="繰り返し期間", null=True, blank=True
    )

    # いつまで繰り返し処理を行うのかを指定する
    # Datetimefieldのdefault値はdatetime型で指定する
    # stop = models.DateTimeField(verbose_name="繰り返し終了日", default=timedelta(days=7), null=True, blank=True)
    stop = models.DateTimeField(
        verbose_name="繰り返し終了日",
        default=timezone.now() + timedelta(days=1000),
        null=True,
        blank=True,
    )

    # スケジュールを登録したユーザー
    # スケジュールを作成したユーザーが削除されたらスケジュールも削除される
    user = models.ForeignKey(
        base.AUTH_USER_MODEL,
        verbose_name="スケジュール作成者",
        on_delete=models.CASCADE,
    )

    all_day = models.BooleanField(verbose_name="終日イベント", default=False)

    def create_json_data(self):
        # スケジュールの詳細を保存する辞書を作成
        details = {}
        # jsでイベントを操作するときに利用するid(schedulemodelのidを利用できる)
        details["id"] = self.id
        details["title"] = self.title
        details["start"] = localtime(self.start).strftime("%Y-%m-%dT%H:%M")
        details["end"] = localtime(self.end).strftime("%Y-%m-%dT%H:%M")
        details["extendedProps"] = {"repeat": False}
        if self.is_repeat != False:
            details["extendedProps"] = {"repeat": True}
        if self.all_day == True:
            details["allDay"] = True

        return details

    def cancels(self):
        return CancelRepeatEvent.objects.filter(event=self.id)

    def is_cancel(self):
        cancels = CancelRepeatEvent.objects.filter(event=self.id)
        flag = False

        # 時差を考慮するためにtimedeltaで時差を追加する

        start_dt = self.start.date()
        for cancel in cancels:
            cancel_dt = cancel.cancel_dt.date()

            if start_dt == cancel_dt:
                flag = True
                break

        return flag

    def __str__(self):
        return self.title


# TODO: メール通知後に記録するモデル。
class EventNotified(models.Model):

    event = models.ForeignKey(
        Event, verbose_name="紐づくスケジュール", on_delete=models.CASCADE
    )
    start_dt = models.DateTimeField(verbose_name="スケジュールの日時")
    user = models.ForeignKey(
        base.AUTH_USER_MODEL, verbose_name="投稿者", on_delete=models.CASCADE
    )


class CancelRepeatEvent(models.Model):
    event = models.ForeignKey(
        Event, verbose_name="紐づくカレンダー", on_delete=models.CASCADE
    )

    cancel_dt = models.DateTimeField(verbose_name="キャンセル日時")

    user = models.ForeignKey(
        base.AUTH_USER_MODEL, verbose_name="投稿者", on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.event)

    def create_json_data(self):
        # スケジュールの詳細を保存する辞書を作成
        details = {}
        # jsでイベントを操作するときに利用するid(schedulemodelのidを利用できる)
        details["id"] = self.id
        details["title"] = self.event.title
        details["start"] = localtime(self.cancel_dt).strftime("%Y-%m-%dT%H:%M")
        # キャンセルしたいイベントの終了時刻を取得する
        cancel_end_date = datetime.combine(
            localtime(self.cancel_dt), localtime(self.event.end).time()
        )
        details["end"] = cancel_end_date.strftime("%Y-%m-%dT%H:%M")
        details["extendedProps"] = {"repeat": True}
        if self.event.all_day == True:
            details["allDay"] = True

        return details


## カレンダーに紐付けるメッセージ
class Chat(models.Model):

    calendar = models.ForeignKey(
        Calendar, verbose_name="カレンダー", on_delete=models.CASCADE
    )
    dt = models.DateTimeField(verbose_name="投稿日時", default=timezone.now)

    user = models.ForeignKey(
        base.AUTH_USER_MODEL, verbose_name="投稿者", on_delete=models.CASCADE
    )
    content = models.CharField(verbose_name="内容", max_length=500)

    def __str__(self):
        return self.content
