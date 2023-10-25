from django.core.management.base import BaseCommand

from ...models import Event, EventNotified, CalendarPermission

from ... import create_new_events

from django.utils import timezone
import time,datetime

from django.core.mail import send_mail

# コマンドクラス。
class Command(BaseCommand):

    # manage.py [このファイル名] を実行した時、↓のhandleメソッドが動く。
    def handle(self, *args, **kwargs):

        while True:
            print("スケジュールチェック")
            # Eventモデルを使って、全Eventを取り出す。
            # TODO: 時間が過ぎているスケジュールは取り出さない。
            events   = Event.objects.all()
            
            # 繰り返しと、繰り返しキャンセルを考慮して、new_eventsを返す関数を別のPythonファイルに作って呼び出せるようにする。
            new_eventsobj   = create_new_events.create(events)
            
            now             = timezone.now()
            check_time      = now + datetime.timedelta(minutes=30)
            
            # new_events からループして、現在時刻と比較する。
            for new_event in new_eventsobj:
                if now < new_event.start and new_event.start < check_time:
                    # TODO: 一度メールで通知をしたスケジュールはDBに記録する。
                    if not EventNotified.objects.filter(event=new_event, start_dt=new_event.start).exists():
                        print("アラート")
                        print(new_event)
                        #TODO: ここでメールで通知する。settings.pyで設定したメール設定に基づき送信する。

                        subject = "スケジュールのお時間です。"
                        message = new_event.title

                        # Permissionに登録されているメールアドレスへ送信する。
                        permissions = CalendarPermission.objects.filter( calendar=new_event.calendar )

                        send_list   = []
                        for permission in permissions:
                            send_list.append(permission.user.email)

                        
                        from_email = "hoge@gmail.com"
                        # 送信先のメールアドレスのリスト
                        recipient_list = send_list
                        send_mail(subject, message, from_email, recipient_list)                        
                        
                        # 1度アラートしたものは記録しておく(DB内のデータをコピーするだけなので今回はバリデーション不要。)
                        event_notified   = EventNotified()

                        event_notified.event  = new_event
                        event_notified.start_dt  = new_event.start
                        event_notified.user      = new_event.user

                        event_notified.save()


            time.sleep(1)