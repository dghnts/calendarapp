from django.shortcuts import render, redirect
from django.views import View
from .forms import EventForm
from .models import Event,Calendar

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

class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "schedule/index.html")

index = IndexView.as_view()

'''
class UsersIndexView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        if request.user !="":
            context["calendars"] = Calendar.objects.filter(user=request.user)
        print(request.user)
        print("こんにちは")
        #print(context)
        return render(request, "users/user_index.html",context)
    
    def post(self, request, *args, **kwargs):
         # TODO:カレンダーの新規作成
         
         # request.POSTを編集するためにコピーする
         copied         = request.POST.copy()
         
         # "user"属性を付与して現在ログイン中のユーザーを設定
         copied["user"] = request.user
         
         form   = CalendarForm(copied)
         
         if not form.is_valid():
             print(form.errors)
             return redirect("users:user_index")
         
         # 保存したカレンダーのデータをとる
         calendar   = form.save()
         
         # ｔカレンとーの投稿者自身に全権限を付与
         dic                = {}
         dic["calendar"]    = calendar
         dic["user"]        = request.user
         dic["read"]        = True
         dic["write"]       = True
         dic["chat"]        = True
         
         form   = CalendarPermissionForm(dic)
         
         if form.is_valid():
            form.save()
         
         
         return redirect("users:user_index")
     
user_index = UsersIndexView.as_view()
'''
# カレンダーを表示させるview
class CalendarView(View):
    def get(self, request, pk, *args, **kwargs):
        context = {}
        event_list = []
        eventsobj = Event.objects.all()
        # 現在表示しているカレンダーのオブジェクトを取得
        calendarobj = Calendar.objects.filter(id=pk).first()
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
        
        context["events"]       = dumps(event_list)
        context["eventsobj"]    = eventsobj
        context["calendar"]     = calendarobj
        return render(request,"schedule/calendar.html",context)

calendar = CalendarView.as_view()

# イベント登録フォーム用のview
class EditEventView(View):
    def post(self, request, pk, *args, **kwargs):
        if pk == 0:
            form = EventForm(request.POST)
            success = "イベントの登録に成功しました"
        else:
            form = EventForm(request.POST, instance=Event.objects.filter(id=pk).first())
            success = "イベントの編集に成功しました"
        # バリデーションチェック
        if not form.is_valid():
            # バリデーションエラーの場合の処理
            #print("イベントの登録に失敗しました")
            
            #エラー内容をjdon形式で取得
            errors = form.errors.get_json_data().values()
            
            for error in errors:
                for e in error:
                    messages.error(request, e["message"])
            
            # pkで表示しているカレンダーのidをurlに渡す
            return redirect("schedule:calendar",pk=pk)
        
        #　バリデーションOK
        messages.info(request, success)
        form.save()
        
        # pkで表示しているカレンダーのidをurlに渡す
        return redirect("schedule:calendar",pk=pk)
        
edit_event = EditEventView.as_view()

# イベント削除用のview
class DeleteEventView(View):
    def post(self, request, pk, *args, **keargs):
        
        # 削除したいイベントを取得
        event = Event.objects.filter(id=pk).first()
        event.delete()
        
        #削除完了メッセージをcalendarｄのページで表示する
        messages.info(request,"イベントを削除しました")
        return redirect("schedule:calendar",pk=pk)
            
delete_event = DeleteEventView.as_view()