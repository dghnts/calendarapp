from django.contrib import admin
from .models import Calendar,Schedule

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

class ScheduleAdmin(admin.ModelAdmin):
    # 指定したフィールドを表示する
    list_display = ["id", "calendar", "start_dt", "end_dt", "content", "user", "repeat", "stop"]
    
    # 指定したフィールドの検索と絞り込み
    search_fields = ["calendar", "start_dt", "end_dt", "user"]
    list_filter   = ["calendar", "start_dt", "end_dt", "user"]
    
    # 1ページあたりに表示する件数
    list_per_page = 10
    # 全権表示を許容する最大件数（目安1000~5000）
    list_max_show_all = 2000
# カレンダーテーブルの管理画面を登録    
admin.site.register(Calendar,CalendarAdmin)
admin.site.register(Schedule,ScheduleAdmin)