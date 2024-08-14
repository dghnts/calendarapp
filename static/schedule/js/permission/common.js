function setupForm(permission_form, authority) {
    const select = permission_form.querySelector("select");

    select.addEventListener("change", function () {
        let value = select.value;
        let read = permission_form.querySelector("[name='read']");
        let write = permission_form.querySelector("[name='write']");
        let chat = permission_form.querySelector("[name='chat']");

        // selectのvalue属性と同じvalueをもつ連想配列を取得する
        const auth = authority.find((obj) => obj["value"] == value);
        console.log(select);
        read.checked = auth["read"];
        write.checked = auth["write"];
        chat.checked = auth["chat"];
    });

    // 全ての入力フォームの削除ボタンを取得する
    const delete_btns = permission_form.querySelectorAll("[name='delete_btn']");

    // 削除ボタンに削除操作を実装する
    delete_btns.forEach((btn) => {
        btn.addEventListener("click", function () {
            btn.parentElement.parentElement.remove();
        });
    });
}

function addPermissionForm(permission_form_area, authority) {
    const value =
        permission_form_area.querySelectorAll(".permission_form").length + 1;

    // permission_formをコピー
    const permission_form_init_area = document
        .querySelector("#permission_form_init_area")
        .children[0].cloneNode(true);
    const authorities = permission_form_init_area.querySelector(".authorities");

    //console.log(authorities);

    // 各valueの値を書き換える。
    authorities.querySelector("[name='authority']").value = value;
    authorities.querySelector("[name='read']").value = value;
    authorities.querySelector("[name='write']").value = value;
    authorities.querySelector("[name='chat']").value = value;

    permission_form_area.appendChild(permission_form_init_area);

    // 追加したformにクリック時の処理を追加する
    const permission_form = permission_form_area.lastElementChild;
    setupForm(permission_form, authority);
}
