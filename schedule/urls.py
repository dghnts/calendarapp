from django.urls import path
from . import views

app_name="schedule"

urlpatterns = [
    path("", views.calendar, name="calendar"),
    path("registerevent/<str:pk>", views.register_event, name="register_event"),
    # イベント毎のview
    path("event/<int:pk>", views.event, name="event"),
    path("event/delete_event/<int:pk>", views.delete_event, name="delete_event"),
]
