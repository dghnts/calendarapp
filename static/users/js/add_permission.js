window.addEventListener('load', function (){
    const permission_form_add   = document.querySelector('#permission_form_add');
    const permission_form_area  = document.querySelector('#permission_form_area');

    permission_form_add.addEventListener("click", () => {
        const value                     = permission_form_area.querySelectorAll(".permission_form").length + 1;

        // permission_formをコピー
        const permission_form_init_area = document.querySelector("#permission_form_init_area").children[0].cloneNode(true);

        // 各valueの値を書き換える。
        permission_form_init_area.querySelector("[name='authority']").value = value;
        permission_form_init_area.querySelector("[name='read']").value      = value;
        permission_form_init_area.querySelector("[name='write']").value     = value;
        permission_form_init_area.querySelector("[name='chat']").value      = value;

        permission_form_area.appendChild(permission_form_init_area);

        // 追加したformにクリック時の処理を追加する
        const permission_form   =   permission_form_area.lastElementChild;

        // select要素を取得
        const select            =   permission_form.querySelector("select");

        select.addEventListener("change", function(){
                let value   = select.value
                let read    = permission_form.querySelector("[name='read']");
                let write   = permission_form.querySelector("[name='write']");
                let chat    = permission_form.querySelector("[name='chat']");

                // selectのvalue属性と同じvalueをもつ連想配列を取得する
                const auth      = authority.find((obj) => obj["value"]==value); 
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
});