from schedule.models import Calendar


def get_calendars(request):
    context = {}
    if not request.user.is_anonymous:
        calendars = Calendar.objects.filter(permission=request.user)
        context["calendars"] = calendars
        context["owner_calendars"] = calendars.filter(user=request.user)
        context["other_calendars"] = calendars.exclude(user=request.user)

    print(context)
    return context
