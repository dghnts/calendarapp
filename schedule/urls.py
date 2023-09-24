from . import views
from django.urls import path

app_name="schedule"

urlpatterns = [
    path("",views.index, name="index"),
    path("calendar/<int:pk>", views.calendar, name="calendar"),
    # イベント削除用のurl
    path("delete_event/<int:pk>/", views.delete_event, name="delete_event"),
]
