from django.shortcuts import render, redirect
from django.views import View
from .forms import ScheduleForm
from .models import Schedule

from django.contrib import messages

from json import dumps

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
        schedule_list = []
        # 全ての登録されたスケジュールに対して以下の処理を実行する
        for schedule in Schedule.objects.all():
            # スケジュールの詳細を保存する辞書を作成
            details = {}
            details["title"] = schedule.content
            details["start"] = schedule.start_dt.strftime('%Y-%m-%d')
            details["end"] = schedule.end_dt.strftime('%Y-%m-%d')
            schedule_list.append(details)
        print(schedule_list)
        
        context["schedule"] = dumps(schedule_list)
        return render(request,"schedule/calendar.html",context)

calendar = CalendarView.as_view()

# イベント登録フォーム用のview
class ReigsterEventView(View):
    def get(self, request, pk, *args, **keargs):
        # contextに日付の情報を渡す
        context = {}
        context["event_date"] = pk
        return render(request, "schedule/event.html", context)
    
    def post(self, request, *args, **kwargs):
        form = ScheduleForm(request.POST)
        
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
