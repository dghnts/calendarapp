from django.contrib import admin
from .models import Calendar, Event, CalendarPermission, CalendarMessage,CancelRepeatEvent

class CalendarAdmin(admin.ModelAdmin):
    # 指定したフィールドを表示する
    list_display = ["id", "user", "name"]
    
    # 指定したフィールドの検索と絞り込み
    search_fields = ["user", "name"]
    list_filter   = ["user", "name"]
    
    # 1ページあたりに表示する件数
    list_per_page = 10
    # 全権表示を許容する最大件数（目安1000~5000）
    list_max_show_all = 2000

class EventAdmin(admin.ModelAdmin):
    # 指定したフィールドを表示する
    list_display = ["id", 
                    "calendar",
                    "start", 
                    "end", 
                    "title", 
                    # "user", 
                    # "repeat", 
                    # "stop",
                    ]
    
    # 指定したフィールドの検索と絞り込み
    #search_fields = ["calendar", "start_dt", "end_dt", "user"]
    #list_filter   = ["calendar", "start_dt", "end_dt", "user"]
    
    # 1ページあたりに表示する件数
    list_per_page = 10
    # 全権表示を許容する最大件数（目安1000~5000）
    list_max_show_all = 2000

class CalendarPermissionAdmin(admin.ModelAdmin):
     # 指定したフィールドを表示する
    list_display = ["calendar","user","read","write","chat"]
    
# カレンダーテーブルの管理画面を登録    
admin.site.register(Calendar, CalendarAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(CalendarPermission, CalendarPermissionAdmin)
admin.site.register(CalendarMessage)
admin.site.register(CancelRepeatEvent)