window.addEventListener("load", function () {
    const permission_form_edit_add = document.querySelector(
        "#permission_form_edit_add"
    );
    const permission_form_edit_area = document.querySelector(
        "#permission_form_edit_area"
    );

    // ユーザー権限の連想配列
    const authority = [
        { value: "3", read: true, write: true, chat: true },
        { value: "0", read: true, write: false, chat: false },
        { value: "1", read: true, write: true, chat: false },
        { value: "2", read: true, write: false, chat: true },
    ];

    // 登録済みの権限の一覧を取得
    const permission_forms =
        permission_form_edit_area.querySelectorAll(".permission_form");

    // 全ての権限に対して以下の処理を行う
    permission_forms.forEach((permission_form) => {
        let selecttag = permission_form.querySelector("select");
        selecttag.addEventListener("change", () => {
            setupForm(permission_form, authority);
        });
    });

    permission_form_edit_add.addEventListener("click", () => {
        addPermissionForm(permission_form_edit_area, authority);
    });
});
