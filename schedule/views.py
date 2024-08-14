from django.shortcuts import render, redirect
from django.views import View
from .forms import EventForm
from .models import (
    Event,
    Calendar,
    CalendarPermission,
    Chat,
    CancelRepeatEvent,
)
from .forms import (
    EventForm,
    CalendarForm,
    CalendarPermissionForm,
    ChatForm,
    CancelRepeatEventForm,
)

from config import settings

from django.contrib import messages

from json import dumps
from django.utils.timezone import localtime
from datetime import datetime, timedelta

from . import create_new_events

from django.http.response import JsonResponse
from django.template.loader import render_to_string

from django.contrib.auth import get_user_model

from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, "schedule/index.html")


index = IndexView.as_view()


# カレンダーを表示させるview
class CalendarView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}
        if not "pk" in kwargs.keys():
            return render(request, "schedule/index.html")
        else:
            pk = kwargs["pk"]
            if not CalendarPermission.objects.filter(
                calendar=pk, user=request.user, read=True
            ).exists():
                messages.error(
                    request,
                    "あなたにはこのカレンダーへのアクセス権（読み込み権限）がありません",
                )
                return redirect("schedule:index")
            # print("読み込み権限の確認")

            # 現在表示しているカレンダーのオブジェクトを取得
            calendarobj = Calendar.objects.filter(id=pk).first()
            # 現在表示しているカレンダーに紐づいているイベントをすべて取得
            eventsobj = Event.objects.filter(calendar=calendarobj)

            # 全ての登録されたスケジュールに対して以下の処理を実行する
            new_eventsobj = create_new_events.create(eventsobj)

            # カレンダーに登録するイベントのデータを登録するリストを作成
            event_list = []
            for event in new_eventsobj:
                event_list.append(event.create_json_data())

            # 繰り返しをキャンセルしたイベントのデータを登録するリストを作成
            event_cancel_list = []
            for cancel_event in CancelRepeatEvent.objects.all():
                event_cancel_list.append(cancel_event.create_json_data())

            context["events"] = dumps(event_list)
            context["events_cancel"] = dumps(event_cancel_list)
            context["eventsobj"] = new_eventsobj
            context["calendar"] = calendarobj
            context["chats"] = Chat.objects.filter(calendar=pk)
            # print(context["events"])
            permissions = CalendarPermission.objects.filter(calendar=pk)

            for permission in permissions:
                # value_sum
                # read = True -> 0
                # read = True -> +1
                # read = true -> +2
                value_sum = (
                    permission.read * 0 + permission.write * 1 + permission.chat * 2
                )
                permission.select = value_sum

            context["calendar_permissions"] = permissions
            context["user_permissions"] = permissions.filter(user=request.user).first()

            return render(request, "schedule/calendar.html", context)

    def post(self, request, pk, *args, **kwargs):
        copied = request.POST.copy()
        copied["user"] = request.user
        copied["start"] = copied["start_day"] + " " + copied["start_time"]
        copied["end"] = copied["end_day"] + " " + copied["end_time"]

        print(request.POST)
        if "all_day" in copied.keys():
            copied["all_day"] = True
            print("これは終日のイベントです")

        calendar_id = request.POST.get("calendar")
        if pk == 0:
            form = EventForm(copied)
            success = "イベントの登録に成功しました"
        else:
            form = EventForm(copied, instance=Event.objects.filter(id=pk).first())
            success = "イベントの編集に成功しました"
        # バリデーションチェック
        print(copied)
        if not form.is_valid():
            # バリデーションエラーの場合の処理
            # print("イベントの登録に失敗しました")

            # エラー内容をjdon形式で取得
            errors = form.errors.get_json_data().values()

            for error in errors:
                for e in error:
                    messages.error(request, e["message"])

            # pkで表示しているカレンダーのidをurlに渡す
            return redirect("schedule:calendar", pk=calendar_id)

        # 　バリデーションOK
        messages.info(request, success)
        form.save()

        # pkで表示しているカレンダーのidをurlに渡す
        return redirect("schedule:calendar", pk=calendar_id)


calendar = CalendarView.as_view()


class CreateCalendarView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        # TODO:カレンダーの新規作成
        # request.POSTを編集するためにコピーする
        # name属性をもつ        -> カレンダーの新規作成
        # name属性をもたない    -> 共有権限の編集
        copied = request.POST.copy()

        # "user"属性を付与して現在ログイン中のユーザーを設定
        copied["user"] = request.user

        form = CalendarForm(copied)

        if not form.is_valid():

            print(form.errors)

            return redirect("schedule:index")

        # 保存したカレンダーのデータをとる

        calendar = form.save()

        # カレンダーの投稿者自身に全権限を付与

        dic = {}
        dic["calendar"] = calendar
        dic["user"] = request.user
        dic["read"] = True
        dic["write"] = True
        dic["chat"] = True

        form = CalendarPermissionForm(dic)

        if form.is_valid():

            form.save()

            # TODO:カレンダーに紐づく権限を付与。
            emails = request.POST.getlist("email")
            authorities = request.POST.getlist("authority")
            reads = request.POST.getlist("read")
            writes = request.POST.getlist("write")
            chats = request.POST.getlist("chat")
            for email, authority in zip(emails, authorities):
                dic = {}
                dic["calendar"] = calendar
                # TODO: カスタムユーザーモデルを使って検索
                print(email)
                print(get_user_model().objects.filter(email=email).first())
                dic["user"] = get_user_model().objects.filter(email=email).first()
                # ↓参照: https://note.nkmk.me/python-if-conditional-expressions/
                dic["read"] = True if authority in reads else False
                dic["write"] = True if authority in writes else False
                dic["chat"] = True if authority in chats else False
                form = CalendarPermissionForm(dic)
                if form.is_valid():
                    form.save()
                    print("成功")
                else:
                    print(form.errors)

        # 　新規作成したカレンダーのページへリダイレクトする
        return redirect("schedule:calendar", calendar.id)


create_calendar = CreateCalendarView.as_view()


class DeleteCalendarView(View):
    def post(self, request, pk, *args, **keargs):
        # 削除したいカレンダーを取得
        calendar_obj = Calendar.objects.filter(id=pk).first()
        calendar_obj.delete()

        # 削除完了メッセージをcalendarのページで表示する
        messages.info(request, "カレンダーを削除しました。")

        return redirect("schedule:index")


delete_calendar = DeleteCalendarView.as_view()


class CalendarPermissionView(View):

    # pkは対象のカレンダー
    def post(self, request, pk, *args, **kwargs):
        # ここでカレンダーの権限の投稿・編集を受け付ける。
        ids = request.POST.getlist("id")
        emails = request.POST.getlist("email")
        authorities = request.POST.getlist("authority")

        reads = request.POST.getlist("read")
        writes = request.POST.getlist("write")
        chats = request.POST.getlist("chat")

        # 現在登録されているpermissionでidsにidがないものは権限を削除する
        for permission in CalendarPermission.objects.filter(calendar=pk):
            if not permission.id in ids:
                permission.delete()
        print(ids)
        for id, email, authority in zip(ids, emails, authorities):
            dic = {}
            dic["calendar"] = pk
            dic["user"] = get_user_model().objects.filter(email=email).first()

            dic["read"] = True if authority in reads else False
            dic["write"] = True if authority in writes else False
            dic["chat"] = True if authority in chats else False

            print(dic)
            if id != "":
                # 編集対象がある場合はそちらを指定する(新規作成の場合はinstanceがNoneになるので、編集と新規作成を両立できる。)
                calendar_permission = CalendarPermission.objects.filter(id=id).first()
            else:
                calendar_permission = None

            # instanceがNone → 新規作成
            # instanceがNoneではない → 対象を編集する
            form = CalendarPermissionForm(dic, instance=calendar_permission)

            if form.is_valid():
                form.save()
                print("編集完了")
            else:
                print(form.errors)

        return redirect("schedule:calendar", pk)


calendar_permission = CalendarPermissionView.as_view()


class CreateChatView(View):

    # pkは対象のカレンダー
    def post(self, request, pk, *args, **kwargs):
        # chat権限がないユーザーはcalendarにリダイレクトする
        if not CalendarPermission.objects.filter(
            calendar=pk, user=request.user, chat=True
        ).exists():
            print("あなたにはこのカレンダーのチャット投稿権限がありません。")
            return redirect("schedule:calendar", pk)

        copied = request.POST.copy()
        copied["user"] = request.user
        copied["calendar"] = pk

        form = ChatForm(copied)

        data = {}
        data["success"] = True

        if form.is_valid():
            messages.info(request, "チャットを送信しました")
            form.save()
        else:
            errors = form.errors.get_json_data().values()

            for error in errors:
                for e in error:
                    messages.error(request, e["message"])
            data["success"] = False

        chats = Chat.objects.all()
        data["content"] = render_to_string(
            "schedule/chat_content.html", {"chats": chats}, request
        )
        data["messages"] = render_to_string(
            "common/message.html", {"messages": messages.get_messages(request)}, request
        )

        return JsonResponse(data)


create_chat = CreateChatView.as_view()


# 繰り返しスケジュールのキャンセルを受け付ける。
class EventRepeatCancelView(View):

    # pkは対象のSchedule
    def post(self, request, pk, *args, **kwargs):
        event = Event.objects.filter(id=pk).first()

        # TODO:キャンセルを保存する。 "cancel_dt"が含まれている。
        copied = request.POST.copy()

        copied["cancel_dt"] = datetime.strptime(
            copied["cancel_dt"].split(" ")[0], "%Y-%m-%d"
        )
        copied["user"] = request.user
        copied["event"] = event

        print(copied["cancel_dt"])
        form = CancelRepeatEventForm(copied)

        if form.is_valid():
            print("指定した日付の繰り返しスケジュールはキャンセルします。")
            form.save()
        else:
            print("登録できませんでした")

        return redirect("schedule:calendar", event.calendar.id)


event_repeat_cancel = EventRepeatCancelView.as_view()


# 繰り返しスケジュールのキャンセルを受け付ける。
class EventRepeatCancelDeleteView(View):

    # pkは対象のScheduleRepeatCancelのid
    def post(self, request, pk, *args, **kwargs):
        event_repeat_cancel = CancelRepeatEvent.objects.filter(
            id=pk, user=request.user
        ).first()
        json = {"error": False}

        if event_repeat_cancel:
            event_repeat_cancel.delete()

        # キャンセルを取り消す繰り返しイベントに紐づいているカレンダーを取得
        calendarobj = Calendar.objects.filter(
            id=event_repeat_cancel.event.calendar.id
        ).first()
        # 現在表示しているカレンダーに紐づいているイベントをすべて取得
        eventsobj = Event.objects.filter(calendar=calendarobj)

        # 全ての登録されたイベントをjson形式に変換
        new_eventsobj = create_new_events.create(eventsobj)

        # カレンダーに登録するイベントのデータを登録するリストを作成
        event_list = []
        for event in new_eventsobj:
            event_list.append(event.create_json_data())

        # 繰り返しをキャンセルしたイベントのデータを登録するリストを作成
        event_cancel_list = []
        for cancel_event in CancelRepeatEvent.objects.all():
            event_cancel_list.append(cancel_event.create_json_data())

        json["events"] = dumps(event_list)
        json["events_cancel"] = dumps(event_cancel_list)

        return JsonResponse(json)


event_repeat_cancel_delete = EventRepeatCancelDeleteView.as_view()


# イベント削除用のview
class DeleteEventView(View):
    def post(self, request, pk, *args, **keargs):
        # 削除したいイベントを取得
        event = Event.objects.filter(id=pk).first()
        # 　イベントを登録しているカレンダーのidを取得する
        calendar_id = event.calendar.id
        # イベントの削除
        event.delete()

        # 削除完了メッセージをcalendarのページで表示する
        messages.info(request, "イベントを削除しました")
        return redirect("schedule:calendar", pk=calendar_id)


delete_event = DeleteEventView.as_view()


# チャット削除用のview
class DeleteChatView(View):
    def post(self, request, pk, *args, **kwargs):
        # 削除したいチャットを削除
        chat = Chat.objects.filter(id=pk).first()
        # 　イベントを登録しているカレンダーのidを取得する
        # calendar_id = chat.calendar.id
        # メッセージの削除
        chat.delete()

        chats = Chat.objects.all()
        # 削除完了メッセージをcalendarのページで表示する
        messages.info(request, "イベントを削除しました")

        data = {}
        data["success"] = True
        data["chats"] = render_to_string(
            "schedule/chat_content.html", {"chats": chats}, request
        )
        data["messages"] = render_to_string(
            "common/message.html", {"messages": messages.get_messages(request)}, request
        )

        return JsonResponse(data)


delete_chat = DeleteChatView.as_view()


class UpdateChatView(View):
    def post(self, request, pk, *args, **kwargs):
        chat = Chat.objects.filter(id=pk).first()

        copied = request.POST.copy()
        copied["user"] = chat.user
        copied["calendar"] = chat.calendar.id

        form = ChatForm(copied, instance=chat)

        data = {}
        data["success"] = True

        if form.is_valid():
            form.save()
            data["content"] = render_to_string(
                "schedule/chat.html", {"chat": chat}, request
            )
        else:
            print(form.errors)
            data["success"] = False

        messages.info(request, "チャットを編集しました")
        data["messages"] = render_to_string(
            "common/message.html", {"messages": messages.get_messages(request)}, request
        )

        return JsonResponse(data)


update_chat = UpdateChatView.as_view()
