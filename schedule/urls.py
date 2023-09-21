from django.urls import path
from . import views

app_name="schedule"

urlpatterns = [
    path("", views.calendar, name="calendar"),
    path("event/<int:pk>", views.edit_event, name="edit_event"),
    # イベント削除用のurl
    path("delete_event/<int:pk>", views.delete_event, name="delete_event"),
]
