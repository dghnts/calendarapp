from . import views
from django.urls import path

app_name = "schedule"

urlpatterns = [
    path("", views.index, name="index"),   
    path("calendar/<int:pk>", views.calendar, name="calendar"),
    path("create_calendar", views.create_calendar, name="createcalendar"),
    path("delete_calendar/<int:pk>", views.delete_calendar, name="delete_calendar"),
    # 編集権限の変更用url
    path(
        "calendar_permission/<int:pk>",
        views.calendar_permission,
        name="calendar_permission",
    ),
    # イベント削除用のurl
    path("delete_event/<int:pk>/", views.delete_event, name="delete_event"),
    # 繰り返しイベントキャンセル用のurl
    path(
        "event_repeat_cancel/<int:pk>/",
        views.event_repeat_cancel,
        name="event_repeat_cancel",
    ),
    # 繰り返しイベント削除用のurl
    path(
        "event_repeat_cancel_delete/<int:pk>/",
        views.event_repeat_cancel_delete,
        name="event_repeat_cancel_delete",
    ),
    # チャット用のURL
    path("create_chat/<int:pk>/", views.create_chat, name="create_chat"),
    path("delete_chat/<int:pk>/", views.delete_chat, name="delete_chat"),
    path("update_chat/<int:pk>/", views.update_chat, name="update_chat")
]
