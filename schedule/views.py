from django.shortcuts import render, redirect
from django.views import View
from .forms import ScheduleForm
from .models import Schedule

from django.contrib import messages

# Create your views here.

# カレンダーを表示させるview
class CalendarView(View):
    def get(self, request, *args, **kwargs):
        return render(request,"schedule/calendar.html")

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
