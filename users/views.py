from django.shortcuts import render,redirect
from django.views import View

from schedule.forms import Calendar, CalendarPermission
from schedule.forms import CalendarForm, CalendarPermissionForm

# Create your views here.
class UsersIndexView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        context["calendars"] = Calendar.objects.all()
        print("OK")
        print(context)
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