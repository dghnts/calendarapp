from django import forms
from .models import Calendar,Event,CalendarPermission,CalendarMessage, CancelRepeatEvent

class CalendarForm(forms.ModelForm):
    
    class Meta:
        model = Calendar
        fields = ["user", "name", "permission"]
        
class EventForm(forms.ModelForm):
    
    class Meta:
        model = Event
        fields = ["calendar",
                    "start", 
                    "end", 
                    "title", 
                    "user",
                    "repeat",
                    "stop",
                  ]
        
        # エラーメッセージ
        error_messages = {
            'title': {
                   'required': "イベントの内容を入力してください",
            },
        }

class CancelRepeatEventForm(forms.ModelForm):
    class Meta:
        model   = CancelRepeatEvent
        fields  = ["event","cancel_dt","user"] 

class CalendarPermissionForm(forms.ModelForm):
    class Meta:
        model   = CalendarPermission
        fields  = [ "calendar","user","read","write","chat" ] 

class CalendarMessageForm(forms.ModelForm):
    class Meta:
        model   = CalendarMessage
        fields  = ["calendar", "user", "content"] 