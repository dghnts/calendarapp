from schedule.models import Calendar, CalendarPermission


def get_context(request):
    context = {}

    if not request.user.is_anonymous:
        # ユーザーが権限を持つカレンダーを取得
        calendars = Calendar.objects.filter(permission=request.user)
        context["calendars"] = calendars
        context["owner_calendars"] = calendars.filter(user=request.user)
        context["other_calendars"] = calendars.exclude(user=request.user)

    for ctx in context:
        print(ctx, ":", context[ctx])
    return context
