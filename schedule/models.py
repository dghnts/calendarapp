from django.db import models
from datetime import datetime,timedelta
from django.utils import timezone

from users.models import CustomUser

from config import settings

# カレンダーモデル
class Calendar(models.Model):
    #作成したユーザー
    #作成者のアカウントが消えたらカレンダーも同時に削除される
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="作成者", on_delete=models.CASCADE)
    #登録するカレンダーの名前
    name = models.CharField(verbose_name="カレンダー", max_length=100)
    
    # カレンダーを共有するユーザー名の指定
    #share = models.ManyToManyField(settings.AUTH_USER_MODEL,verbose_name="公開範囲", related_name="share_calendar")
    
    permission = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name="公開範囲", through="CalendarPermission" ,related_name="calendar_permission", blank=True)
    
    def __str__(self):
        return self.name
    
class CalendarPermission(models.Model):
    
    calendar    = models.ForeignKey(Calendar, verbose_name="カレンダー", on_delete=models.CASCADE)
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="対象ユーザー", on_delete=models.CASCADE)
    
    read        = models.BooleanField(verbose_name="読み込み権限", default=False)
    write       = models.BooleanField(verbose_name="書き込み権限", default=False)
    chat        = models.BooleanField(verbose_name="チャット権限", default=False)
    
    def __str__(self):
        return self.calendar.name
    
# スケジュールモデル
class Event(models.Model):
    ###############################################################
    # field名はfullcalendarのプロパティに合わせる（propertyが存在しないものは最下部にまとまておく
    ###############################################################
    
    #スケジュールを登録するカレンダー
    #カレンダーが削除されると同時にスケジュールも削除される    
    calendar = models.ForeignKey(Calendar, verbose_name="スケジュール", on_delete=models.CASCADE)
    
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
    # durationsfieldのdefault値はtimedelta型で指定する
    # repeat =  models.DurationField(verbose_name="繰り返し期間", default="", null=True, blank=True)
    #repeat =  models.DurationField(verbose_name="繰り返し期間", default=timedelta(days=7), null=True, blank=True)
    repeat =  models.PositiveIntegerField(verbose_name="繰り返し期間", null=True, blank=True)
    
    # いつまで繰り返し処理を行うのかを指定する
    # Datetimefieldのdefault値はdatetime型で指定する
    #stop = models.DateTimeField(verbose_name="繰り返し終了日", default=timedelta(days=7), null=True, blank=True)
    stop = models.DateTimeField(verbose_name="繰り返し終了日", default=timezone.now()+timedelta(days=1000), null=True, blank=True)
    
    # スケジュールを登録したユーザー
    # スケジュールを作成したユーザーが削除されたらスケジュールも削除される
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="スケジュール作成者", on_delete=models.CASCADE)
    
    def cancels(self):
        return CancelRepeatEvent.objects.filter(event=self.id)
    
    def is_cancel(self):
        cancels = CancelRepeatEvent.objects.filter(event=self.id)
        flag    = False
        
        # 時差を考慮するためにtimedeltaで時差を追加する
        
        start_dt    = self.start+timedelta(hours=9)
        start_dt    = start_dt.date()
        for cancel in cancels:
            cancel_dt   = cancel.cancel_dt
    
            if start_dt == cancel_dt:
                flag    = True
                break
    
        return flag
    
class CancelRepeatEvent(models.Model):
    event       = models.ForeignKey(Event, verbose_name="紐づくカレンダー", on_delete=models.CASCADE)
    
    cancel_dt   = models.DateField(verbose_name="キャンセル日時")
    
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="投稿者", on_delete=models.CASCADE)
    
## カレンダーに紐付けるメッセージ
class CalendarMessage(models.Model):

    calendar    = models.ForeignKey(Calendar, verbose_name="カレンダー", on_delete=models.CASCADE)
    dt          = models.DateTimeField(verbose_name="投稿日時",default=timezone.now)

    user        = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="投稿者", on_delete=models.CASCADE)
    content     = models.CharField(verbose_name="内容", max_length=500)
    
    def __str__(self):
        return self.content