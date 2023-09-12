from django.db import models
from datetime import datetime, timedelta

from users.models import CustomUser

# カレンダーモデル
class Calendar(models.Model):
    #作成したユーザー
    #作成者のアカウントが消えたらカレンダーも同時に削除される
    user = models.ForeignKey(CustomUser, verbose_name="作成者", on_delete=models.CASCADE)
    #登録するカレンダーの名前
    name = models.CharField(verbose_name="カレンダー", max_length=100)
    
    # カレンダーを共有するユーザー名の指定
    share = models.ManyToManyField(CustomUser,verbose_name="公開範囲", related_name="share_calendar")

# スケジュールモデル
class Schedule(models.Model):
    #スケジュールを登録するカレンダー
    #カレンダー額削除されると同時にスケジュールも削除される    
    # calendar = models.ForeignKey(Calendar, verbose_name="スケジュール", on_delete=models.CASCADE)
    
    # スケジュールの開始日
    # 日時はユーザーが指定するから，auto_now,auto_now_addはFalse
    start_dt = models.DateTimeField(verbose_name="開始日時", auto_now=False, auto_now_add=False)
    
    # スケジュールの終了日
    # 日時はゆーザーが指定するから，auto_now,auto_now_addはFalse
    end_dt = models.DateTimeField(verbose_name="開始日時", auto_now=False, auto_now_add=False)
    
    # スケジュールの内容（要約）
    content = models.CharField(max_length=200)
    
    # スケジュールを登録したユーザー
    # スケジュールを作成したユーザーが削除されたらスケジュールも削除される
    #user = models.ForeignKey(CustomUser, verbose_name="スケジュール作成者", on_delete=models.CASCADE)
    
    ## 定期的に設定されるスケジュールに対する処理
    ## 繰り返し処理ではない場合，空欄で提出
    
    ## どのくらいのスパンで繰り返すか指定
    ## 繰り返しの初期値を7日間で設定
    #repeat =  models.DurationField(verbose_name="繰り返し期間", default="", null=True, blank=True)
    
    # いつまで繰り返し処理を行うのかを指定する
    #stop = models.DateTimeField(verbose_name="繰り返し終了日", default="", null=True, blank=True)