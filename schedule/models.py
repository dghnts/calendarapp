from django.db import models
from datetime import timedelta
from django.utils import timezone

from users.models import CustomUser


# カレンダーモデル
class Calendar(models.Model):
    #作成したユーザー
    #作成者のアカウントが消えたらカレンダーも同時に削除される
    user = models.ForeignKey(CustomUser, verbose_name="作成者", on_delete=models.CASCADE)
    #登録するカレンダーの名前
    name = models.CharField(verbose_name="カレンダー", max_length=100)
    
    # カレンダーを共有するユーザー名の指定
    #share = models.ManyToManyField(CustomUser,verbose_name="公開範囲", related_name="share_calendar")
    
    permission = models.ManyToManyField(CustomUser, verbose_name="公開範囲", through="CalendarPermission" ,related_name="calendar_permission", blank=True)
    
    def __str__(self):
        return self.name
    
class CalendarPermission(models.Model):
    
    calendar    = models.ForeignKey(Calendar, verbose_name="カレンダー", on_delete=models.CASCADE)
    user        = models.ForeignKey(CustomUser, verbose_name="対象ユーザー", on_delete=models.CASCADE)
    
    read        = models.BooleanField(verbose_name="読み込み権限", default=False)
    write        = models.BooleanField(verbose_name="書き込み権限", default=False)
    chat        = models.BooleanField(verbose_name="チャット権限", default=False)
    
    def __str__(self):
        return self.calendar.name
    
# スケジュールモデル
class Event(models.Model):
    ###############################################################
    # field名はfullcalendarのプロパティに合わせる（propertyが存在しないものは最下部にまとまておく
    ###############################################################
    
    #スケジュールを登録するカレンダー
    #カレンダー額削除されると同時にスケジュールも削除される    
    # calendar = models.ForeignKey(Calendar, verbose_name="スケジュール", on_delete=models.CASCADE)
    
    # スケジュールの開始日
    # 日時はユーザーが指定するから，auto_now,auto_now_addはFalse
    start = models.DateTimeField(verbose_name="開始日時", auto_now=False, auto_now_add=False)
    
    # スケジュールの終了日
    # 日時はゆーザーが指定するから，auto_now,auto_now_addはFalse
    end = models.DateTimeField(verbose_name="開始日時", auto_now=False, auto_now_add=False)
    
    # スケジュールの内容（要約）
    title = models.CharField(max_length=200)
    
    ## 定期的に設定されるスケジュールに対する処理
    ## 繰り返し処理ではない場合，空欄で提出
    
    ## どのくらいのスパンで繰り返すか指定
    ## 繰り返しの初期値を7日間で設定
    # durationsfieldのdefault値はtimedeltaｓ型で指定する
    # repeat =  models.DurationField(verbose_name="繰り返し期間", default="", null=True, blank=True)
    repeat =  models.DurationField(verbose_name="繰り返し期間", default=timedelta(days=7), null=True, blank=True)
    
    # いつまで繰り返し処理を行うのかを指定する
    # Datetimefieldのdefault値はdatetimeｓ型でｓ
    #stop = models.DateTimeField(verbose_name="繰り返し終了日", default=timedelta(days=7), null=True, blank=True)
    stop = models.DateTimeField(verbose_name="繰り返し終了日", default=timezone.now()+timedelta(days=1000), null=True, blank=True)
    
    # スケジュールを登録したユーザー
    # スケジュールを作成したユーザーが削除されたらスケジュールも削除される
    # user = models.ForeignKey(CustomUser, verbose_name="スケジュール作成者", on_delete=models.CASCADE)