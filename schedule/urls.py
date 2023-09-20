from django.urls import path
from . import views

app_name="schedule"

urlpatterns = [
    path("", views.calendar, name="calendar"),
    path("registerevent", views.register_event, name="register_event"),
    # イベント削除用のurl
    path("delete_event/<int:pk>", views.delete_event, name="delete_event"),
]
