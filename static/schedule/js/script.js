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
    let config_dt = { 
        enableTime: true,
        dateFormat: "Y-m-d H:i",
        locale: "ja",
        position: "center",
        defaultDate: dt,
    };

    //        ↓発動させたい要素       　↓設定
    flatpickr("[name='end']", config_dt);
    flatpickr("[name='start']", config_dt);
    flatpickr("[name='stop']", config_dt);
     // カレンダーに関する設定 ///////////////////////////////////////////////////////////////////
    // カレンダーの要素を取得
    var calendarEl = document.querySelector('#calendar');
    let delete_event_form = document.delete_event
 
    // オブジェクトを作成 Fullcalendarを実行。引数は要素と表示するカレンダーの設定
    var calendar = new FullCalendar.Calendar(calendarEl,{
        headerToolbar: {
            start: 'prev,next today',
            center: 'title',
            end: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        // 表示言語の設定
        locale: "ja",
        buttonIcons: true,
        initialView: "dayGridMonth",
        //日付の（複数）選択を可能にする
        selectable: true,
        select: function(info) {
            //console.log(info.end)
            //console.log(info.start)
            // 開始日を指定する（時間は現在時刻）
            info.start.setHours(info.start.getHours() + today.getHours() );

            // 終了日を指定する（デフォルトは選択範囲の最終日）
            info.end.setDate(info.end.getDate());
            info.end.setHours(info.end.getHours()+today.getHours());

            // イベントの開始日と終了日をflatpickrで設定できるようにする
            config_dt.defaultDate = info.start;
            flatpickr("[name='start']", config_dt);

            config_dt.defaultDate = info.end;
            flatpickr("[name='end']", config_dt);
            flatpickr("[name='stop']", config_dt);
            
            //イベント作成用のviewへのリンクをaction属性に設定(id=0)
            document.event_edit.action = edit_event;
            //console.log(document.edit_event.action);
             
            //新規作成時は削除ボタンを非表示にする
            delete_event_form.style.display ="none";

            // モーダルをクリックする
            document.querySelector('#register').click();
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
            config_dt.defaultDate = info.event.start;
            // 開始日と終了日を設定する
            flatpickr("[name='start']", config_dt);
            //　終了日の値がnullでなければ終了日を入力する。
            if(info.event.end != null){
                config_dt.defaultDate = info.event.end;
            }
            // nullの場合は開始日と同じにする
            else{
                config_dt.defaultDate = info.event.start;
            }
            console.log(config_dt.defaultDate);
            flatpickr("[name='end']", config_dt);
            flatpickr("[name='stop']", config_dt);

            // イベントのタイトルを取得して表示する
            document.querySelector("[name='title']").value = info.event.title;
            
            //イベント編集用のviewへのリンクをaction属性に設定(id=0)
            edit_event = edit_event.replace("0", event_id);
            document.event_edit.action = edit_event;

            console.log(info.event.extendedProps.repeat);
            // DTLを利用して作成したURLを編集してイベント削除のURLを作成する
            if (info.event.extendedProps.repeat){
                // イベントのもとのidを取得
                //default_event_id            = event_id.split("_")[0]
                config_dt.defaultDate = info.event.start;
                flatpickr("[name='cancel_dt']", config_dt);
                //document.querySelector("[name='cancel_dt']").value=info.event.start
                event_repeat_cancel         = event_repeat_cancel.replace('0', event_id);
                delete_event_form.action    = event_repeat_cancel;
                console.log(event_repeat_cancel);
            }else{
                delete_event = delete_event.replace('0', event_id);
                delete_event_form.action = delete_event;
                console.log(delete_event_form.action);
            }
            
            // 削除ボタンが非表示の場合に表示を切り替える
            if(delete_event_form.style.display == "none"){
                delete_event_form.style.display = "";
            }

            document.querySelector('#register').click();

        },
        editable: true,
        dayMaxEvents: true,
    });
    calendar.render();

    var event_listEl = document.querySelector('#event_list');
    var event_list = new FullCalendar.Calendar(event_listEl,{
        headerToolbar: {
            left: 'prev,today,next',
            center: 'title',
            right: 'listMonth,listWeek,listDay'
        },
        // 表示言語の設定
        locale: "ja",
        height: "100%",
        buttonIcons: true,
        initialView: "listMonth",
        events: events,
        //イベントをクリックしたときの処理
        eventClick: function(info) {
            event_id = info.event.id;
            title = info.event.title;
            config_dt.defaultDate = info.event.start;
            // 開始日と終了日を設定する
            flatpickr("[name='start']", config_dt);
            //　終了日の値がnullでなければ終了日を入力する。
            if(info.event.end != null){
                config_dt.defaultDate = info.event.end;
            }
            // nullの場合は開始日と同じにする
            else{
                config_dt.defaultDate = info.event.start;
            }
            console.log(config_dt.defaultDate);
            flatpickr("[name='end']", config_dt);
            flatpickr("[name='stop']", config_dt);

            // イベントのタイトルを取得して表示する
            document.querySelector("[name='title']").value = info.event.title;
            
            //イベント編集用のviewへのリンクをaction属性に設定(id=0)
            edit_event = edit_event.replace("0", event_id);
            document.event_edit.action = edit_event;

            console.log(info.event.extendedProps.repeat);
            // DTLを利用して作成したURLを編集してイベント削除のURLを作成する
            if (info.event.extendedProps.repeat){
                // イベントのもとのidを取得
                //default_event_id            = event_id.split("_")[0]
                config_dt.defaultDate = info.event.start;
                flatpickr("[name='cancel_dt']", config_dt);
                //document.querySelector("[name='cancel_dt']").value=info.event.start
                event_repeat_cancel         = event_repeat_cancel.replace('0', event_id);
                delete_event_form.action    = event_repeat_cancel;
                console.log(event_repeat_cancel);
            }else{
                delete_event = delete_event.replace('0', event_id);
                delete_event_form.action = delete_event;
                console.log(delete_event_form.action);
            }
            
            // 削除ボタンが非表示の場合に表示を切り替える
            if(delete_event_form.style.display == "none"){
                delete_event_form.style.display = "";
            }

            document.querySelector('#register').click();
        },
    });
    event_list.render();

    all_day_check = document.querySelector("[name=all_day]");
    all_day_check.addEventListener("click",function(){
        if(all_day_check.checked){
            let start_dt    = document.querySelector('[name=start]').value;
            let defaulttime = start_dt.split(" ")[1];
            start_dt        = start_dt.replace(defaulttime, "00:00");
            let end_dt    = document.querySelector('[name=end]').value;
            defaulttime = end_dt.split(" ")[1];
            end_dt        = end_dt.replace(defaulttime, "00:00");
            document.querySelector('[name=start]').value  = start_dt;
            document.querySelector('[name=end]').value  = end_dt;
            console.log("終日のイベントにします");
        }
    });
});