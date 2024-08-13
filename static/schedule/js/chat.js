document.addEventListener("DOMContentLoaded", () => {
    //設定ボタン推したとき，設定メニューの表示・非表示を切り替える
    setSettignsButton();

    document
        .querySelector("#create_chat_form")
        .addEventListener("submit", function (e) {
            e.preventDefault();

            const submitter = this.querySelector(".btn");
            const body = new FormData(this, submitter);

            fetch("/create_chat/" + calendarId + "/", {
                method: "POST",
                body: body,
            })
                .then((res) => res.json())
                .then((data) => {
                    console.log(data.content);
                    if (data.success) {
                        const chatContainer =
                            document.querySelector(".chat_container");

                        //入力フォームの初期化
                        this.reset();

                        //チャットデータのセット
                        chatContainer.innerHTML = data.content;
                        setSettignsButton();
                    } else {
                        alert("Failed to update chat.");
                    }
                })
                .catch((error) => console.error("Error:", error));
        });
});

function setSettignsButton() {
    document.querySelectorAll(".settings_button").forEach((button) => {
        button.addEventListener("click", function () {
            var chatId = this.dataset.id;
            var menu = document.querySelector(
                '.settings_menu[data-id="' + chatId + '"]'
            );

            menu.style.display =
                menu.style.display === "block" ? "none" : "block";
        });
    });

    // 編集ボタンを押したとき，メニューと元のコンテンツを非表示にする
    document.querySelectorAll(".update_link").forEach((link) => {
        link.addEventListener("click", function (e) {
            e.preventDefault();
            var chatId = this.dataset.id;
            var chatDiv = document.querySelector("#chat_" + chatId);
            var contentP = chatDiv.querySelector("#chat_content_" + chatId);
            var updateForm = chatDiv.querySelector("#update_form_" + chatId);
            var menu = document.querySelector(
                '.settings_menu[data-id="' + chatId + '"]'
            );

            menu.style.display = "none";
            contentP.style.display = "none";
            updateForm.style.display = "block";
        });
    });

    document.querySelectorAll(".update_form").forEach((form) => {
        form.addEventListener("submit", function (e) {
            e.preventDefault();

            const chatId = this.dataset.id;
            const form = document.querySelector("#update_form_" + chatId);
            const submitter = document.querySelector(
                "[name=update_submit_" + chatId + "]"
            );
            const body = new FormData(form, submitter);

            fetch("/update_chat/" + chatId + "/", {
                method: "POST",
                body: body,
            })
                .then((res) => res.json())
                .then((data) => {
                    console.log(data.content);
                    if (data.success) {
                        const chatDiv = document.getElementById(
                            "chat_content_" + chatId
                        );
                        chatDiv.innerHTML = data.content;
                        chatDiv.style.display = "block";
                        form.style.display = "none";
                    } else {
                        alert("Failed to update chat.");
                    }
                })
                .catch((error) => console.error("Error:", error));
        });
    });

    document.querySelectorAll(".delete_link").forEach((link) => {
        link.addEventListener("click", function (e) {
            e.preventDefault();

            const chatId = this.dataset.id;
            const form = document.querySelector(
                "[name=delete_chat_" + chatId + "]"
            );
            const submitter = form.querySelector(".btn");
            const body = new FormData(form, submitter);

            fetch("/delete_chat/" + chatId + "/", {
                method: "POST",
                body: body,
            })
                .then((res) => res.json())
                .then((data) => {
                    if (data.success) {
                        console.log(data);
                        const chatContainer =
                            document.querySelector(".chat_container");

                        chatContainer.innerHTML = data.chats;
                        setSettignsButton();

                        // 削除成功のメッセージを表示する
                        const messages = new DOMParser().parseFromString(
                            data.messages,
                            "text/html"
                        ).body.firstElementChild;

                        // headerタグの後にmessageを表示させる
                        document
                            .querySelector("html header")
                            .insertAdjacentElement("afterend", messages);
                    } else {
                        alert("Failed to update chat.");
                    }
                })
                .catch((error) => console.error("Error:", error));
        });
    });
}
