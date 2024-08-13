document.addEventListener("DOMContentLoaded", () => {
    //設定ボタン推したとき，設定メニューの表示・非表示を切り替える
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
        link.addEventListener("click", function (event) {
            event.preventDefault();
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
            const submitter = document.querySelector("[name=update_submit_"+ chatId + "]");
            const body = new FormData(form,submitter);

            var csrfToken = this.querySelector(
                "[name=csrfmiddlewaretoken]"
            ).value;
            
            fetch("/update_chat/" + chatId + "/", {
                method: "POST",
                body: body,
            })
                .then((res) => res.json())
                .then((data) => {
                    console.log(data.content);
                    if (data.success) {
                        const chatDiv    = document.getElementById("chat_content_" + chatId);
                        chatDiv.innerHTML = data.content;
                        chatDiv.style.display = "block"
                        form.style.display = "none"
                        
                    } else {
                        alert("Failed to update chat.");
                    }
                })
                .catch((error) => console.error("Error:", error));
        })
    });
});

