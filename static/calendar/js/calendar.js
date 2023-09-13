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
            console.log(info.start);
            start_day = info.startStr.split("T");

            // urlの作成
            const url = "http://127.0.0.1:8000/registerevent/"+start_day[0];
            
            //クリックした日付のイベントを作成するページに移動する
            //window.location.href = url;
        },
        events: events,
        //イベントをクリックしたときの処理
        eventClick: function(info) {
            id = info.event.id
            console.log(id);
            //イベント詳細ページへ移動する
            window.location.href = "http://127.0.0.1:8000/event/"+id
        },
        editable: true,
        dayMaxEvents: true,
    });
    calendar.render();
});