/*
function delete_permission(n) {
    //フォームの数を取得
    const input_length = document.querySelectorAll("#permission_form_input").length;

    //フォームが1個なら処理終了
    if (input_length === 1) {
        return;

    } else {
        //div#input-form内の一番下の要素を取得
        const delete_form = document.getElementsByClassName(``);

        console.log(`delete_permission_${n}`)
        console.log(delete_form);
        //要素を削除
        //delete_form.remove();
        //console.log(document.querySelectorAll("#permission_form_input"))
    }
}*/

window.addEventListener('load', function(){
    const permission_form_edit_add   = document.querySelector('#permission_form_edit_add');
    const permission_form_edit_area  = document.querySelector('#permission_form_edit_area');

    // 登録済みの権限の一覧を取得
    const permission_forms = permission_form_edit_area.querySelectorAll(".permission_form");

    // ユーザー権限の連想配列
    const authority = [
        {"value":"3", "read":true, "write":true, "chat":true},
        {"value":"0", "read":true, "write":false, "chat":false},
        {"value":"1", "read":true, "write":true, "chat":false},
        {"value":"2", "read":true, "write":false, "chat":true}
    ]
    
    // 全ての権限に対して以下の処理委を行う
    permission_forms.forEach((permission_form) => {
        let selecttag = permission_form.querySelector("select");
        selecttag.addEventListener("change", () =>{
            let value   = selecttag.value
            let read    = permission_form.querySelector("[name='read']");
            let write   = permission_form.querySelector("[name='write']");
            let chat    = permission_form.querySelector("[name='chat']");
            
            // selectのvalue属性と同じvalueをもつ連想配列を取得する
            const auth  = authority.find((obj) => obj["value"]==value); 

            read.checked    = auth["read"];
            write.checked   = auth["write"];
            chat.checked    = auth["chat"];
        });

        // 全ての入力フォームの削除ボタンを取得する
        delete_btns     =   permission_form.querySelectorAll("[name='delete_btn']");

         // 削除ボタンに削除操作を実装する
        delete_btns.forEach(btn => {
                btn.addEventListener('click', function(){
                console.log(btn.parentElement);
                btn.parentElement.remove();
            });
        }); 
    });


    permission_form_edit_add.addEventListener("click", () => {
        console.log("hello")
        const value                     = permission_form_edit_area.querySelectorAll(".permission_form").length + 1;

        // permission_formをコピー
        const permission_form_init_area = document.querySelector("#permission_form_init_area").children[0].cloneNode(true);

        // 各valueの値を書き換える。
        permission_form_init_area.querySelector("[name='authority']").value = value;
        permission_form_init_area.querySelector("[name='read']").value      = value;
        permission_form_init_area.querySelector("[name='write']").value     = value;
        permission_form_init_area.querySelector("[name='chat']").value      = value;
        
        // 各checkboxをtrueにしておく
        permission_form_init_area.querySelector("[name='read']").checked    = true;
        permission_form_init_area.querySelector("[name='write']").checked   = true;
        permission_form_init_area.querySelector("[name='chat']").checked    = true;
        
        permission_form_edit_area.appendChild(permission_form_init_area);

        // 追加したformにクリック時の処理を追加する
        const permission_form_last     =   permission_form_edit_area.lastElementChild;

        // select要素を取得
        const select          =   permission_form_last.querySelector("select");

        select.addEventListener("change", function(){
            let value       = select.value
            let read        = permission_form_last.querySelector("[name='read']");
            let write       = permission_form_last.querySelector("[name='write']");
            let chat        = permission_form_last.querySelector("[name='chat']");

            // selectのvalue属性と同じvalueをもつ連想配列を取得する
            const auth      = authority.find((obj) => obj["value"]==value); 

            read.checked    = auth["read"];
            write.checked   = auth["write"];
            chat.checked    = auth["chat"];
        });

        // 全ての入力フォームの削除ボタンを取得する
        delete_btns     =   permission_form_last.querySelectorAll("[name='delete_btn']");

        // 削除ボタンに削除操作を実装する
        delete_btns.forEach(btn => {
            btn.addEventListener('click', function(){
                console.log(btn.parentElement);
                btn.parentElement.remove();
            });
        }); 
    });
});