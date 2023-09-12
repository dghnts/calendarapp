from django import forms
from .models import Calendar,Schedule

class CalendarForm(forms.ModelForm):
    
    class Meta:
        model = Calendar
        fields = ["user", "name", "share"]
        
class ScheduleForm(forms.ModelForm):
    
    class Meta:
        model = Schedule
        fields = [#"calendar"#,
                  "start_dt", 
                  "end_dt", 
                  "content", 
                  #"user", "repeat", "stop",
                  ]
        
        # エラーメッセージ
        error_messages = {
            'content': {
                   'required': "イベントの内容を入力してください",
            },
        }
