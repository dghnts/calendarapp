window.addEventListener("load" , function (){ 
    //flatpckrの設定/////////////////////////////////////////////////////////////////
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
        position: "center",
        defaultDate: dt,
    };

    // イベント終了時用の設定
    let config_end_dt = { 
        enableTime: true,
        dateFormat: "Y-m-d H:i",
        locale: "ja",
        position: "above center",
        defaultDate: dt,
    };

    //        ↓発動させたい要素       　↓設定
    //flatpickr("[name='end_dt']", config_dt);
    //flatpickr("[name='start_dt']", config_dt);
    
     // カレンダーに関する設定 ///////////////////////////////////////////////////////////////////
    // カレンダーの要素を取得
    var calendarEl = document.getElementById('calendar');
    let delete_event_form = document.delete_event
 
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
            console.log(info.end)
            console.log(info.start)
            // 開始日を指定する（時間は現在時刻）
            info.start.setHours(info.start.getHours() + today.getHours() );

            // 終了日を指定する（デフォルトは選択範囲の最終日）
            info.end.setDate(info.end.getDate());
            info.end.setHours(info.end.getHours()+today.getHours());
            config_start_dt.defaultDate = info.start;
            config_end_dt.defaultDate = info.end;

            // イベントの開始日と終了日をflatpickrで設定できるようにする
            flatpickr("[name='start']", config_start_dt);
            flatpickr("[name='end']", config_end_dt);
            
            //イベント作成用のviewへのリンクをaction属性に設定(id=0)
            document.edit_event.action = edit_event;
            //console.log(document.edit_event.action);
             
            //新規作成時は削除ボタンを非表示にする
            delete_event_form.style.display ="none";

            // モーダルをクリックする
            document.getElementById("register").click();
        },

        dateClick: function(info) {
            // 時間のセット
            //console.log(info.date);
        },
        
        events: events,
        //イベントをクリックしたときの処理
        eventClick: function(info) {
            event_id = info.event.id;
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

            // イベントのタイトルを取得して表示する
            document.getElementsByName("title")[0].value = info.event.title;
            //console.log(document.getElementsByName("title")[0]);
            
            //イベント編集用のviewへのリンクをaction属性に設定(id=0)
            edit_event = edit_event.replace("0", event_id);
            document.edit_event.action = edit_event;
 
            // DTLを利用して作成したURLを編集してイベント削除のURLを作成する
            delete_event = delete_event.replace('0', event_id);
            delete_event_form.action = delete_event;
            
            // 削除ボタンが非表示の場合に表示を切り替える
            if(delete_event_form.style.display == "none"){
                delete_event_form.style.display = "";
            }

            document.getElementById("register").click();

        },
        editable: true,
        dayMaxEvents: true,
    });
    calendar.render();
    // 各イベントの編集ボタンの一覧を取得する
    //console.log(document.querySelectorAll('[id^="edit_"]'));
    
    // 各ボタンに対してクリックイベント処理を追加
    document.querySelectorAll('[id^="edit_"]').forEach(function(event_btn) {
            event_btn.addEventListener('click', function(){
                // idからeventobjectのidを取り出す
                let event_id = this.id.split("_")[1];

                // event_idに紐づいたevent情報を取得する
                let event = calendar.getEventById(event_id);

                config_start_dt.defaultDate = event.start;
                // 開始日と終了日を設定する
                flatpickr("[name='start']", config_start_dt);
                //　終了日の値がnullでなければ終了日を入力する。
                if(event.end != null){
                    config_end_dt.defaultDate = event.end;
                }
                // nullの場合は開始日と同じにする
                else{
                    config_end_dt.defaultDate = event.start;
                }
                console.log(config_end_dt.defaultDate);
                flatpickr("[name='end']", config_end_dt);

                // イベントのタイトルを取得して表示する
                document.getElementsByName("title")[0].value = event.title;

                //イベント編集用のviewへのリンクをaction属性に設定(id=0)
                edit_event = edit_event.replace("0", event_id);
                document.edit_event.action = edit_event;

                // DTLを利用して作成したURLを編集してイベント削除のURLを作成する
                delete_event = delete_event.replace('0', event_id);
                delete_event_form.action = delete_event;
        })
    });
});