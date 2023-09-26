from django.shortcuts import render,redirect
from django.views import View

from schedule.forms import Calendar, CalendarPermission
from schedule.forms import CalendarForm, CalendarPermissionForm

from config import settings

# Create your views here.
class UsersIndexView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        #print(request.user.is_anonymous)
        if not request.user.is_anonymous:
            print(request.user)
            #print(Calendar.objects.filter(calendarpermission=""))
            context["calendars"] = Calendar.objects.filter(permission=request.user)

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
        
        # カレンダーの投稿者自身に全権限を付与
        dic                = {}
        dic["calendar"]    = calendar
        dic["user"]        = request.user
        dic["read"]        = True
        dic["write"]       = True
        dic["chat"]        = True
        
        form   = CalendarPermissionForm(dic)
         
        if form.is_valid():
            form.save()
            
        print(request.POST)

        # TODO:カレンダーに紐づく権限を付与。

        emails  = request.POST.getlist("email")
        authorities = request.POST.getlist("authority")
        

        for email,authority in zip(emails,authorities) :
            
            dic             = {}
            dic["calendar"] = calendar

            #TODO: カスタムユーザーモデルを使って検索
            print(email)

            print( settings.AUTH_USER_MODEL.objects.filter(email=email).first() )
            dic["user"]     = settings.AUTH_USER_MODEL.objects.filter(email=email).first()
            dic["read"]     = False
            dic["write"]    = False
            dic["chat"]     = False
            
            if not authority == "":
                dic["read"] = True
            
            if authority == "all" or authority=="read and write":
                dic["write"]    = True

            
            if authority == "all" or authority=="read and chat":
                dic["chat"]     = True
                
            print(dic)
            form    = CalendarPermissionForm(dic)

            if form.is_valid():
                form.save()
                print("成功")
            else:
                print(form.errors)
                         
        return redirect("users:user_index") 
     
user_index = UsersIndexView.as_view()