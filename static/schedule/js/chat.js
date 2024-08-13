document.addEventListener("DOMContentLoaded", () => {
    //設定ボタン推したとき，設定メニューの表示・非表示を切り替える
    setSettignsButton();

    document
        .querySelector("#create_chat_form")
        .addEventListener("submit", function (e) {
            e.preventDefault();

            const url = "/create_chat/" + calendarId + "/";
            const submitter = this.querySelector(".btn");
            const body = new FormData(this, submitter);

            fetch(url, {
                method: "POST",
                body: body,
            })
                .then((res) => res.json())
                .then((data) => {
                    if (data.success) {
                        const chatContainer =
                            document.querySelector(".chat_container");

                        //入力フォームの初期化
                        this.reset();
                        //チャットデータのセット
                        chatContainer.innerHTML = data.content;
                        setSettignsButton();

                        sendMessage(data);
                    } else {
                        sendMessage(data);
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
            const chatId = this.dataset.id;
            const contentP = document.querySelector("#chat_content_" + chatId);
            const form = document.querySelector("#update_chat_" + chatId);
            const menu = document.querySelector(
                '.settings_menu[data-id="' + chatId + '"]'
            );

            menu.style.display = "none";
            contentP.style.display = "none";
            form.style.display = "block";
        });
    });

    document.querySelectorAll(".update_form").forEach((form) => {
        form.addEventListener("submit", function (e) {
            e.preventDefault();

            const chatId = this.dataset.id;
            const url = "/update_chat/" + chatId + "/";
            const form = document.querySelector("#update_chat_" + chatId);
            const submitter = form.querySelector(
                "[name=update_button_" + chatId + "]"
            );
            const body = new FormData(form, submitter);

            fetch(url, {
                method: "POST",
                body: body,
            })
                .then((res) => res.json())
                .then((data) => {
                    if (data.success) {
                        const chatDiv = document.querySelector(
                            "#chat_content_" + chatId
                        );
                        chatDiv.innerHTML = data.content;
                        chatDiv.style.display = "block";
                        form.style.display = "none";

                        sendMessage(data);
                    } else {
                        sendMessage(data);
                    }
                })
                .catch((error) => console.error("Error:", error));
        });
    });

    document.querySelectorAll(".delete_link").forEach((link) => {
        link.addEventListener("click", function (e) {
            e.preventDefault();

            const chatId = this.dataset.id;
            const url = "/delete_chat/" + chatId + "/";
            const form = document.querySelector("#delete_chat_" + chatId);
            const submitter = form.querySelector(
                "[name=delete_button" + chatId + "]"
            );
            const body = new FormData(form, submitter);

            fetch(url, {
                method: "POST",
                body: body,
            })
                .then((res) => res.json())
                .then((data) => {
                    if (data.success) {
                        const chatContainer =
                            document.querySelector(".chat_container");

                        chatContainer.innerHTML = data.chats;
                        setSettignsButton();

                        sendMessage(data);
                    } else {
                        endMessage("data");
                    }
                })
                .catch((error) => console.error("Error:", error));
        });
    });
}

function sendMessage(data) {
    const messagesList = document.querySelector(".messages");

    if (messagesList) {
        messagesList.remove();
    }
    // 削除成功のメッセージを表示する
    const messages = new DOMParser().parseFromString(data.messages, "text/html")
        .body.firstElementChild;

    // headerタグの後にmessageを表示させる
    document
        .querySelector("html header")
        .insertAdjacentElement("afterend", messages);
}
