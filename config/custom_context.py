from schedule.models import Calendar

def get_calendars(request):
    if not request.user.is_anonymous:
        return {"calendars" : Calendar.objects.filter(permission=request.user)}
    else:
        return dict()