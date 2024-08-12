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

    document.querySelectorAll(".update_link").forEach((link) => {
        link.addEventListener("click", function (event) {
            event.preventDefault();
            var messageId = this.dataset.id;
            var messageDiv = document.getElementById("message_" + messageId);
            var contentP = messageDiv.querySelector(".message_content");
            var updateForm = messageDiv.querySelector(".update_form");
            var menu = document.querySelector(
                '.settings_menu[data-id="' + messageId + '"]'
            );

            menu.style.display = "none";
            contentP.style.display = "none";
            updateForm.style.display = "block";
        });
    });

/*    
    document.querySelectorAll(".update_form").forEach((form) => {
        form.addEventListener("submit", function () {

            const form = this.parelentElement;
            var messageId = this.dataset.id;
            var newContent = this.querySelector('[name="content"]').value;
            var csrfToken = this.querySelector(
                "[name=csrfmiddlewaretoken]"
            ).value;
            
            fetch("/update_message/" + messageId + "/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken,
                },
            })
                .then((res) => {
                    res_json = res.json();
                    console.log(res_json);
                })
                .then((data) => {
                    console.log(data);
                    if (data.success) {
                        var messageDiv = document.getElementById(
                            "message-" + messageId
                        );
                        messageDiv.outerHTML = data.content;
                    } else {
                        alert("Failed to update message.");
                    }
                })
                .catch((error) => console.error("Error:", error));
        });
    });*/
});

