from . import views
from django.urls import path

app_name="schedule"

urlpatterns = [
    path("",views.index, name="index"),
    path("calendar/", views.calendar, name="calendar_index"),
    path("calendar/<int:pk>", views.calendar, name="calendar"),
    path("create_calendar", views.createcalendar, name="createcalendar"),
    # 編集権限の変更用url
    path("calendar_permission/<int:pk>", views.calendar_permission, name="calendar_permission"),
    # イベント削除用のurl
    path("delete_event/<int:pk>/", views.delete_event, name="delete_event"),
    # 繰り返しイベント削除用のurl
    #path("cancel_repeat_event/")
    #チャット用のURL
    path("calendar_message/<int:pk>/", views.calendar_message, name="calendar_message"),
]
