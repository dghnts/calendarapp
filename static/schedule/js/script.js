window.addEventListener("load" , function (){ 
    //flatpckrの設定/////////////////////////////////////////////////////////////////
    /*今日の日付を取得
    let today = new Date();

    let year    = String(today.getFullYear());
    let month   = ("0" + String(today.getMonth() + 1) ).slice(-2);
    let start_day     = ("0" + String(today.getDate()) ).slice(-2);
    let hour    = ("0" + String(today.getHours()) ).slice(-2);
    let minute  = ("0" + String(today.getMinutes()) ).slice(-2);

    let dt = year + "-" + month + "-" + start_day + " " + hour + ":" + minute; 
    */

    let all_day_check       = document.querySelector("[name='all_day']");
    let start_day                 = document.getElementById("start_day");
    let start_time          = document.getElementById("start_time");
    let end_time            = document.getElementById("end_time");
    let end_day             = document.getElementById("end_day");
    let start_dt            = document.querySelector("[name='start']");
    let end_dt              = document.querySelector("[name='end']");
    //let stop                = document.querySelector("[name=stop");

    // イベント開始日用の設定
    let config_dt   = { 
        //enableTime: true,
        altInput    : true,   
        altFormat   : "Y-m-d",
        dateFormat  : "Y-m-d", //変更
        locale      : "ja",
        position    : "center",
        //defaultDate : dt
    };

    let config_time = {
        altInput    : true,
        altFormat   : "H:i",
        enableTime  : true,
        noCalendar  : true, //カレンダーを表示しない
        dateFormat  : "H:i",
        time_24hr   : true, //24時間表記
    };

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
            //イベント登録画面の初期化
            event_modal_reset();

            // イベントの開始日と終了日をflatpickrで設定できるようにする
            all_day_check.checked   = false,
            config_dt.defaultDate   = info.start;
            config_time.defaultDate   = info.start;
            flatpickr("#start_day", config_dt);
            flatpickr("#start_time", config_time);

            config_dt.defaultDate   = info.end;
            config_time.defaultDate   = info.end;
            flatpickr("#end_day", config_dt);
            flatpickr("#end_time", config_time);
            
            console.log(start_time.value);

            //初期値の設定
            start_dt.value  = start_day.value   + " "   + start_time.value;
            end_dt.value    = end_day.value     + " "   + end_time.value;

            //イベント作成用のviewへのリンクをaction属性に設定(id=0)
            document.event_edit.action = edit_event;

            //新規作成時は削除ボタンを非表示にする
            delete_event_form.style.display ="none";

            if(info.allDay){
                if(!all_day_check.checked){
                    all_day_check.click();
                }
                //　画面に表示する日付を修正する
                // 参考：https://fullcalendar.io/docs/select-callback
                info.end.setDate(info.end.getDate()-1);
                config_dt.defaultDate = info.end;
                //　終了日を入力
                flatpickr("#end_day", config_dt);
                end_dt.value  = end_day.value;
            }else{
                if(all_day_check.checked){
                    all_day_check.click();
                }                
            }
            flatpickr("[name='stop']", config_dt);
            // モーダルをクリックする
            document.querySelector('#register').click();
        },
        
        events: events,
        //イベントをクリックしたときの処理
        eventClick: function(info) {
            event_click(info);
        },
        editable: true,
        dayMaxEvents: true,
    });
    calendar.render();

    var event_list_calendar_El = document.querySelector('#event_list_calendar');
    var event_list_calendar = new FullCalendar.Calendar(event_list_calendar_El,{
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
            event_click(info);
        }
    });
    event_list_calendar.render();

    let event_cancel_calendar_El = document.getElementById('event_cancel_calendar');
    let event_cancel_calendar = new FullCalendar.Calendar(event_cancel_calendar_El, {
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
        events: events_cancel,
        //イベントをクリックしたときの処理
        eventClick: function(info) {
            event_id            = info.event.id;
            const csrftoken = Cookies.get('csrftoken');
            const url       = event_repeat_cancel_delete_url.replace("0",event_id)

            var res             = confirm("このイベントの繰り返しキャンセルを取り消しますか？");
            if(res){
                const request   = new XMLHttpRequest();
                
                //送信先とメソッドの指定
                request.open("POST",url);
            
                //ヘッダにCSRFトークンをセットする。
                request.setRequestHeader("X-CSRFToken", csrftoken);
            
                //送信(内容)
                request.send();
            
                //成功時の処理
                request.onreadystatechange = function() {
                    if( request.readyState === 4 && request.status === 200 ) {
                        let json = JSON.parse(request.responseText);
                        
                        // 更新したキャンセルイベントのjasondataを変数に格納
                        let new_cancel_events = JSON.parse(json["events_cancel"]);

                        // event_cancel_calendarのイベントを削除し、新しいものに更新する
                        let event_cancel_calendar_source = event_cancel_calendar.getEventSources();
                        event_cancel_calendar_source.forEach((source) => {
                            source.remove();
                        });
                        event_cancel_calendar.addEventSource(new_cancel_events);

                        // 更新したイベントのjsondataを変数に格納
                        let new_events = JSON.parse(json["events"]);
                        
                        // calendar,event_list_calendarのイベントを削除し、新しいものに更新する
                        let calendar_source = calendar.getEventSources();
                        calendar_source.forEach((source) => {
                            source.remove();
                        });
                        new_events = JSON.parse(json["events"]);
                        calendar.addEventSource(new_events);

                        let event_list_calendar_source = event_list_calendar.getEventSources();
                        event_list_calendar_source.forEach((source) => {
                            source.remove();
                        });
                        event_list_calendar.addEventSource(new_events);
                    }
                }
            }
        }
    });
    event_cancel_calendar.render();



    all_day_check.addEventListener("click",() =>{change_end_date_format();});

    start_day.onchange = function(){
        if(all_day_check.checked){
            start_dt.value    = start_day.value;
        }else{
            start_dt.value    = start_day.value + " " + start_time.value;
            end_dt.value      = end_day.value   + " " + end_time.value;
    }};

    start_time.onchange = function(){
        start_dt.value  = start_day.value + " " + start_time.value;
    };

    end_time.onchange   = function(){
        end_dt.value    = end_day.value + " " + end_time.value;
    };

    end_day.onchange     = function(){
        end_dt.value  = end_day.value;
    };

    //終了日の入力方法を変更する（時間or日付）
    function change_end_date_format(){
        if(all_day_check.checked){
            // altinputの要素を取得して非表示にする
            start_time.nextSibling.style.display = "none";
            end_time.nextSibling.style.display = "none";
            start_dt.value                            = start_day.value;
            end_dt.value                              = end_day.value;
        }else{
            // altinputの要素を取得して非表示にする
            start_time.nextSibling.style.display = "inline";
            end_time.nextSibling.style.display ="inline";
            start_dt.value                      = start_day.value   + " " + start_time.value;
            end_dt.value                        = end_day.value     + " " + end_time.value;
        }
    };

    // イベント登録画面の初期化
    function event_modal_reset(){
        //終日ボタンにチェックがついていたらチェックを外す
        if(all_day_check.checked){
            all_day_check.checked=false;
        };
        // title欄を空白にする
        document.querySelector("[name='title']").value = "";
    }

    function event_click(info){
        event_id = info.event.id;
        title = info.event.title;

        // 開始日と終了日を設定する
        config_dt.defaultDate = info.event.start;

        // 開始日の日付を設定
        flatpickr("#start_day", config_dt);

        //　終了日の日付を設定
        if(!info.event.end){
            //　info.event.endが存在しない場合、開始日と同じ値を入力する
            flatpickr("#end_day", config_dt);
        }else{
            //　info.event.endが存在する場合、その値を入力する
            config_dt.defaultDate = info.event.end;
            flatpickr("#end_day", config_dt);
        }
        

        config_time.defaultDate = info.event.start;
        flatpickr("#start_time", config_time);
        config_time.defaultDate = info.event.end;
        flatpickr("#end_time", config_time);

        if(info.event.allDay==true){
            console.log("これは終日イベントです");
            if(!all_day_check.checked){
                all_day_check.click();
            }
        }else{
            if(all_day_check.checked){
                all_day_check.click();
            }
        }
        
        // イベントのタイトルを取得して表示する
        document.querySelector("[name='title']").value = info.event.title;
        
        //イベント編集用のviewへのリンクをaction属性に設定(id=0)
        edit_event = edit_event.replace("0", event_id);

        document.event_edit.action = edit_event;
        // HTML側で作成したURLを編集してイベント削除のURLを作成する
        if (info.event.extendedProps.repeat){
            document.querySelector("[name='cancel_dt']").value = start_day.value;
            delete_event_form.action    = event_repeat_cancel_url.replace('0', event_id);
        }else{
            delete_event_form.action = delete_url.replace('0', event_id);            ;
            console.log(delete_event_form.action);
        }
        
        flatpickr("[name='stop']",config_dt);
        
        // 削除ボタンが非表示の場合に表示を切り替える
        if(delete_event_form.style.display == "none"){
            delete_event_form.style.display = "";
        }

        document.querySelector('#register').click();
    }
});