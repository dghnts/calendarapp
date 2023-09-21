from django import forms
from .models import Calendar,Event

class CalendarForm(forms.ModelForm):
    
    class Meta:
        model = Calendar
        fields = ["user", "name" ,"share"]
        
class EventForm(forms.ModelForm):
    
    class Meta:
        model = Event
        fields = [#"calendar"#,
                  "start", 
                  "end", 
                  "title", 
                  # "user",
                  # "repeat",
                  # "stop",
                  ]
        
        # エラーメッセージ
        error_messages = {
            'title': {
                   'required': "イベントの内容を入力してください",
            },
        }
