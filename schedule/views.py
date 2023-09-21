from django.shortcuts import render, redirect
from django.views import View
from .forms import EventForm
from .models import Event

from django.contrib import messages

from json import dumps
from django.utils.timezone import localtime

'''
# modelのフィールド一覧を取得するための関数
def get_fields_name(models):
    # 各フィールドのmeta情報を取得
    meta_fields = models._meta.get_fields()
    
    #for data in meta_fields:
    #    print(type(data))
    
    fields = list()
    
    # enumerate型を利用して各フィールドの名前を取得
    for i, meta_field in enumerate(meta_fields):
        # id以外のすべてのフィールドを取得
        if i > 0:
            fields.append(meta_field.name)
            
    return fields
'''

# カレンダーを表示させるview
class CalendarView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        event_list = []
        eventsobj = Event.objects.all()
        # 全ての登録されたスケジュールに対して以下の処理を実行する
        for event in eventsobj:
            # スケジュールの詳細を保存する辞書を作成
            details = {}
            # jsでイベントを操作するときに利用するid(schedulemodelのidを利用できる)
            details["id"] = event.id
            details["title"] = event.title
            details["start"] = localtime(event.start).strftime('%Y-%m-%d')
            details["end"] = localtime(event.end).strftime('%Y-%m-%d')
            event_list.append(details)
        print(event_list)
        
        context["events"] = dumps(event_list)
        context["eventsobj"] = eventsobj
        return render(request,"schedule/calendar.html",context)

calendar = CalendarView.as_view()

# イベント登録フォーム用のview
class ReigsterEventView(View):
    def get(self, request, pk, *args, **keargs):
        # contextに日付の情報を渡す
        context = {}
        context["event_date"] = pk
        return render(request, "schedule/register_event.html", context)
    
    def post(self, request, *args, **kwargs):
        form = EventForm(request.POST)
        
        # バリデーションチェック
        if not form.is_valid():
            # バリデーションエラーの場合の処理
            #print("イベントの登録に失敗しました")
            
            #エラー内容をjdon形式で取得
            errors = form.errors.get_json_data().values()
            
            for error in errors:
                for e in error:
                    messages.error(request, e["message"])
                    
            return redirect("schedule:calendar")
        
        #　バリデーションOK
        messages.info(request, "イベントの登録に成功しました")
        form.save()
        
        return redirect("schedule:calendar")
        
register_event = ReigsterEventView.as_view()


# イベント登録フォーム用のview
class EventView(View):
    def get(self, request, pk, *args, **keargs):
        # 詳細を表示したいイベントをidから取得する
        event = Event.objects.filter(id=pk).first()
        context = {"event": event}
        return render(request, "schedule/event.html",context)
    
            
event = EventView.as_view()

# イベント削除用のview
class DeleteEventView(View):
    def post(self, request, pk, *args, **keargs):
        
        # 削除したいイベントを取得
        event = Event.objects.filter(id=pk).first()
        event.delete()
        
        #削除完了メッセージをcalendarｄのページで表示する
        messages.info(request,"イベントを削除しました")
        return redirect("schedule:calendar")
            
delete_event = DeleteEventView.as_view()