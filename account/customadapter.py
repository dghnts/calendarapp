from allauth.account.adapter import DefaultAccountAdapter
from schedule.models import Calendar

class CustomAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(selff, request):
        #resolved_url = super().get_login_redirect_url(request)
        # ログインユーザーが権限をもつカレンダーのidを1つURLに書く
        
        if Calendar.objects.filter(permission=request.user).exists():
            calendar_id = Calendar.objects.filter(permission=request.user)[0].id
            return "/calendar/"+str(calendar_id)
        else:
            return "/calendar/"
    