document.addEventListener('DOMContentLoaded', function(){
    // カレンダーの要素を取得
    var calendarEl = document.getElementById('calendar');

    // オブジェクトを作成 Fullcalendarを実行。引数は要素と表示するカレンダーの設定
    var calendar = new FullCalendar.Calendar(calendarEl,{
        headerToolbar: {
            left: 'prev,today,next',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        // 表示言語の設定
        locale: "ja",
        buttonIcons: true,
        initialView: "dayGridMonth",
        //日付の（複数）選択を可能にする
        selectable: true,
        select: function(args) {
            /*var title = prompt('イベント名')
            if (title) {
                calendar.addEvent({
                    title: title,
                    start: args.start,
                    end: args.end,
                    alllDay: args.allDay
                })
            calendar.unselect()
            */

           //日付をクリックしたら，その日付のイベントを作成するページに移動する
           const url = "http://127.0.0.1:8000/event/"+args.start
           console.log(url);
           //イベントの日付を取得する
           console.log(args.start);
           window.location.href = url;
        },
        eventClick: function(arg) {
            if (confirm('本当にこのイベントを削除しますか？')) {
              arg.event.remove()
            }
        },
        editable: true,
        dayMaxEvents: true,
    });
    calendar.render();
});