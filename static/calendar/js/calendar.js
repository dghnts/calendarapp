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
        select: function(info) {
            /*
            var title = prompt('イベント名')
            if (title) {
                calendar.addEvent({
                    title: title,
                    start: info.start,
                    end: info.end,
                    alllDay: info.allDay
                })
            calendar.unselect()
            */

            // 日付をyyyy-mm-dd形式にformatする
            start_day = info.startStr.split("T");

            // urlの作成
            const url = "http://127.0.0.1:8000/event/"+start_day[0];
            
            //クリックした日付のイベントを作成するページに移動する
            window.location.href = url;
        },
        events: schedule,
        //イベントをクリックしたときの処理
        eventClick: function(arg) {
            //イベント詳細ページへ移動する
        },
        editable: true,
        dayMaxEvents: true,
    });
    calendar.render();
});