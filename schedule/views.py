from django.shortcuts import render,redirect
from django.views import View
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
        return redirect("schedule:calendar")
        
register_event = ReigsterEventView.as_view()