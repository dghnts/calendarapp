from . import views
from django.urls import path

app_name="schedule"

urlpatterns = [
    path("",views.index, name="index"),
    path("calendar/<int:pk>", views.calendar, name="calendar"),
    # 編集権限の変更用url
    path("calendar_permission/<int:pk>", views.calendar_permission, name="calendar_permission"),

    # イベント削除用のurl
    path("delete_event/<int:pk>/", views.delete_event, name="delete_event"),
]
