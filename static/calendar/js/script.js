window.addEventListener("load" , function (){ 
    //今日の日付を取得
    let today = new Date();

    let year    = String(today.getFullYear());
    let month   = ("0" + String(today.getMonth() + 1) ).slice(-2);
    let day     = ("0" + String(today.getDate()) ).slice(-2);
    let hour    = ("0" + String(today.getHours()) ).slice(-2);
    let minute  = ("0" + String(today.getMinutes()) ).slice(-2);

    let dt = year + "-" + month + "-" + day + " " + hour + ":" + minute; 
    
    // イベント開始日用の設定
    let config_start_dt = { 
        enableTime: true,
        dateFormat: "Y-m-d H:i",
        locale: "ja",
        defaultDate: dt,
    };

    // イベント終了時用の設定
    let config_end_dt = { 
        enableTime: true,
        dateFormat: "Y-m-d H:i",
        locale: "ja",
        defaultDate: dt,
    };

    //        ↓発動させたい要素       　↓設定
    //flatpickr("[name='end_dt']", config_dt);
    //flatpickr("[name='start_dt']", config_dt);

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
            // 開始日を指定する（時間は現在時刻）
            info.start.setHours(info.start.getHours() + today.getHours() );

            // 終了日を指定する（デフォルトは選択範囲の最終日）
            info.end.setDate(info.end.getDate()-1);
            info.end.setHours(info.end.getHours()+today.getHours());
            config_start_dt.defaultDate = info.start;
            config_end_dt.defaultDate = info.end;
            // イベントの開始日と終了日をflatpickrで設定できるようにする
            flatpickr("[name='start']", config_start_dt);
            flatpickr("[name='end']", config_end_dt);
            
            // モーダルをクリックする
            document.getElementById("register").click();
        },

        dateClick: function(info) {
            // 時間のセット
            console.log(info.date);
        },

        events: events,
        //イベントをクリックしたときの処理
        eventClick: function(info) {
            id = info.event.id;
            title = info.event.title;
            config_start_dt.defaultDate = info.event.start;
            // 開始日と終了日を設定する
            flatpickr("[name='start']", config_start_dt);
            //　終了日の値がnullでなければ終了日を入力する。
            if(info.event.end != null){
                config_end_dt.defaultDate = info.event.end;
            }
            // nullの場合は開始日と同じにする
            else{
                config_end_dt.defaultDate = info.event.start;
            }
            console.log(config_end_dt.defaultDate);
            flatpickr("[name='end']", config_end_dt);
            document.getElementById("register").click();
            
            // Q.urlをベタ打ちしない方法はないのだろうか？=>modalイベントクリック時にjsで取得したidをdjangoに渡したい
            document.delete_event.action = `http://127.0.0.1:8000/delete_event/${id}`;
        },
        editable: true,
        dayMaxEvents: true,
    });
    calendar.render();

});