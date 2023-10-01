window.addEventListener("DOMContentLoaded", () => {
    const sidebar_chk = document.getElementById("sidebar_chk");
    const calendar_area = document.querySelector(".calendar_area");
    console.log(sidebar_chk.checked);
    
    sidebar_chk.addEventListener("click", () => {
        console.log("こんにちは");
        calendar_area.style.width="75%";
        calendar_area.style.marginLeft="25%";
    });
});