from django.shortcuts import render, redirect
from django.views import View
from .forms import EventForm
from .models import Event, Calendar, CalendarPermission, CalendarMessage
from .forms import EventForm, CalendarForm, CalendarPermissionForm, CalendarMessageForm

from users.models import CustomUser

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
        
        if not request.user.is_anonymous:
            #print(Calendar.objects.filter(calendarpermission=""))
            context["calendars"] = Calendar.objects.filter(permission=request.user)
        
        # カレンダーのidが0の時，pkをユーザーの読み込めるidに書き換える
        if pk == 0:
            pk = CalendarPermission.objects.filter(user=request.user ,read=True)[0].calendar.id

        if not CalendarPermission.objects.filter(calendar=pk, user=request.user ,read=True).exists():
            messages.error(request, "あなたにはこのカレンダーへのアクセス権（読み込み権限）がありません")
            return redirect("schedule:index")
        print("読み込み権限の確認")
        
        context["write"] = True
        # 書き込み権限がない場合は編集writeをFalseに変更する
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
        #print(event_list)
        
        context["events"]               = dumps(event_list)
        context["eventsobj"]            = eventsobj
        context["calendar"]             = calendarobj
        context["calendar_messages"]    = CalendarMessage.objects.filter(calendar=pk)
        permissions             = CalendarPermission.objects.filter(calendar=pk)
                
        for permission in permissions:
            # value_sum
            # read = True -> 0
            # read = True -> +1
            # read = true -> +2 
            value_sum   =   (permission.read*0 + permission.write*1 + permission.chat*2)
            permission.select = value_sum
                
        context["permissions"]  = permissions
        
        return render(request,"schedule/calendar.html",context)

    def post(self, request, pk, *args, **kwargs):
        print(request.POST["calendar"])
        calendar_id = request.POST["calendar"]
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
            return redirect("schedule:calendar",pk=calendar_id)
        
        #　バリデーションOK
        messages.info(request, success)
        form.save()
        
        # pkで表示しているカレンダーのidをurlに渡す
        return redirect("schedule:calendar",pk=calendar_id)

calendar = CalendarView.as_view()

class CalendarPermissionView(View):
    
    # pkは対象のカレンダー
    def post(self, request, pk, *args, **kwargs):
        # ここでカレンダーの権限の投稿・編集を受け付ける。
        ids     = request.POST.getlist("id")
        emails  = request.POST.getlist("email")
        authorities = request.POST.getlist("authority")
        
        reads   = request.POST.getlist("read")
        writes  = request.POST.getlist("write")
        chats   = request.POST.getlist("chat")
        
        # 現在登録されているpermissionでidsにidがないものは権限を削除する
        for permission in CalendarPermission.objects.filter(calendar=pk):
            if not permission.id in ids:
                permission.delete()
         
        for id,email,authority in zip(ids,emails,authorities):
            dic             = {}
            dic["calendar"] = pk
            dic["user"]     = CustomUser.objects.filter(email=email).first()
            
            dic["read"]     = True if authority in reads else False 
            dic["write"]    = True if authority in writes else False
            dic["chat"]     = True if authority in chats else False
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
            else:
                print(form.errors)


        return redirect("schedule:calendar", pk)

calendar_permission = CalendarPermissionView.as_view()

   
# イベント削除用のview
class DeleteEventView(View):
    def post(self, request, pk, *args, **keargs):
        
        # 削除したいイベントを取得
        event = Event.objects.filter(id=pk).first()
        #　イベントを登録しているカレンダーのidを取得する
        calendar_id = event.calendar.id
        # イベントの削除
        event.delete()
        
        #削除完了メッセージをcalendarのページで表示する
        messages.info(request,"イベントを削除しました")
        return redirect("schedule:calendar",pk=calendar_id)
            
delete_event = DeleteEventView.as_view()

class CalendarMessageView(View):

    # pkは対象のカレンダー
    def post(self, request, pk, *args, **kwargs):
        # ここでカレンダーのメッセージの投稿を受け付ける。
        
        # chat権限がないユーザーはcalendarにリダイレクトする
        if not CalendarPermission.objects.filter(calendar=pk, user=request.user, chat=True).exists():
            print("あなたにはこのカレンダーのチャット投稿権限がありません。")
            return redirect("schedule:calendar", pk)

        copied              = request.POST.copy()
        copied["user"]      = request.user
        copied["calendar"]  = pk

        form    = CalendarMessageForm(copied)
        
        if form.is_valid():
            form.save()
        else:
            # バリデーションエラーの場合の処理
            #print("イベントの登録に失敗しました")
            
            #エラー内容をjdon形式で取得
            errors = form.errors.get_json_data().values()
            
            for error in errors:
                for e in error:
                    messages.error(request, e["message"])

        return redirect("schedule:calendar", pk)

calendar_message    = CalendarMessageView.as_view()

