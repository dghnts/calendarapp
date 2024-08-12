document.addEventListener("DOMContentLoaded", () => {
    //設定ボタン推したとき，設定メニューの表示・非表示を切り替える
    document.querySelectorAll(".settings_button").forEach((button) => {
        button.addEventListener("click", function () {
            var messageId = this.dataset.id;
            var menu = document.querySelector(
                '.settings_menu[data-id="' + messageId + '"]'
            );

            menu.style.display =
                menu.style.display === "block" ? "none" : "block";
        });
    });

    // 編集ボタンを押したとき，メニューと元のコンテンツを非表示にする
    document.querySelectorAll(".update_link").forEach((link) => {
        link.addEventListener("click", function (event) {
            event.preventDefault();
            var messageId = this.dataset.id;
            var messageDiv = document.querySelector("#message_" + messageId);
            var contentP = messageDiv.querySelector("#message_content_" + messageId);
            var updateForm = messageDiv.querySelector("#update_form_" + messageId);
            var menu = document.querySelector(
                '.settings_menu[data-id="' + messageId + '"]'
            );

            menu.style.display = "none";
            contentP.style.display = "none";
            updateForm.style.display = "block";
        });
    });

    
    document.querySelectorAll(".update_form").forEach((form) => {
        form.addEventListener("submit", function (e) {
            e.preventDefault();
            
            const messageId = this.dataset.id;
            const form = document.querySelector("#update_form_" + messageId);
            const submitter = document.querySelector("[name=update_submit_"+ messageId + "]");
            const body = new FormData(form,submitter);

            var csrfToken = this.querySelector(
                "[name=csrfmiddlewaretoken]"
            ).value;
            
            fetch("/update_message/" + messageId + "/", {
                method: "POST",
                body: body,
            })
                .then((res) => res.json())
                .then((data) => {
                    console.log(data.content);
                    if (data.success) {
                        const messageDiv    = document.getElementById("message_content_" + messageId);
                        messageDiv.innerHTML = data.content;
                        messageDiv.style.display = "block"
                        form.style.display = "none"
                        
                    } else {
                        alert("Failed to update message.");
                    }
                })
                .catch((error) => console.error("Error:", error));
        })
    });
});

