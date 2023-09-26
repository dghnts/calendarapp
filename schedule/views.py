from django.shortcuts import render, redirect
from django.views import View
from .forms import EventForm
from .models import Event, Calendar, CalendarPermission
from .forms import EventForm, CalendarForm, CalendarPermissionForm

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

# カレンダーを表示させるview
class CalendarView(View):
    def get(self, request, pk, *args, **kwargs):
        context = {}
       
        if not CalendarPermission.objects.filter(calendar=pk, user=request.user ,read=True).exists():
            messages.error(request, "あなたにはこのカレンダーへのアクセス権（読み込み権限）がありません")
            return redirect("users:user_index")
        print("読み込み権限の確認")
        
        if not CalendarPermission.objects.filter(calendar=pk, user=request.user, write=True).exists():
            context["write"] = False
        

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

calendar = CalendarView.as_view()

class CalendarPermissionView(View):

    # pkは対象のカレンダー
    def post(self, request, pk, *args, **kwargs):
        # ここでカレンダーの権限の投稿・編集を受け付ける。
        
        ids     = request.POST.getlist("id")
        emails  = request.POST.getlist("email")
        '''
        reads   = request.POST.getlist("read")
        writes  = request.POST.getlist("write")
        chats   = request.POST.getlist("chat")
        '''
        authorities = request.POST("authority")
        
        for id,email,authority in zip(ids,emails,authorities) :
                
            dic             = {}
            dic["calendar"] = pk
            dic["user"]     = CustomUser.objects.filter(email=email).first()
            dic["read"]     = True
            dic["write"]    = False
            dic["chat"]     = False
            print(authority)
            if authority == "all" or authority=="read and write":
                dic["write"]    = True

            
            if authority == "all" or authority=="read and chat":
                dic["chat"]     = True
            
            print(dic)

            if id != "":
                # 編集対象がある場合はそちらを指定する(新規作成の場合はinstanceがNoneになるので、編集と新規作成を両立できる。)
                calendar_permission = CalendarPermission.objects.filter(id=id).first()
            else:
                calendar_permission = None

            # instanceがNone → 新規作成
            # instanceがNoneではない → 対象を編集する
            form    = CalendarPermissionForm(dic, instance=calendar_permission)

            if form.is_valid():
                print("編集完了")
                calendar_permission = form.save()
                print(calendar_permission)
            else:
                print(form.errors)


        return redirect("scheduler:calendar", pk)


calendar_permission = CalendarPermissionView.as_view()

   
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