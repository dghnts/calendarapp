from django.urls import path
from . import views

app_name="schedule"

urlpatterns = [
    path("", views.calendar, name="calendar"),
    path("event/<str:pk>", views.register_event, name="register_event")
]
