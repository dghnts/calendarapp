from django.core.management.base import BaseCommand

import time

from django.utils import timezone

from datetime import timedelta

from ...models import Event

from ...new_events import new_events

# コマンドクラス。
class Command(BaseCommand):

    # manage.py [このファイル名] を実行した時、↓のhandleメソッドが動く。
    def handle(self, *args, **kwargs):
        print("これでコマンドが実行できる。")

        # スケジュールのチェックを1秒おきにするには？
        # ここでwhileループさせる。

        while True:
            print("スケジュールチェック")
            # DBへアクセス。Eventモデルを使って、全Eventを取り出す。
            # XXX: 時間が過ぎているスケジュールは取り出さない。
            print(Event.objects.all())
            events   = Event.objects.all()
            # 繰り返しと、繰り返しキャンセルを考慮して、new_eventsを返す関数を別のPythonファイルに作って呼び出せるようにする。

            new_eventsobj = new_events(events)
            
            
            # new_events からループして、現在時刻と比較する。
            for new_event in new_eventsobj:
                diff    = timezone.now()-new_event.start
                if diff < timedelta(0):
                    continue
                
                if diff <= timedelta(minutes=30):
                    print("30分前です")
                else:
                    print(new_event.title+"は30分前ではありません")
                    print(new_event.start)


            time.sleep(1)