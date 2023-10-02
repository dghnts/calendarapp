window.addEventListener("DOMContentLoaded", () => {
    const sidebar_chk = document.getElementById("sidebar_chk");
    const calendar_area = document.querySelector(".calendar_area");
    
    sidebar_chk.addEventListener("click", () => {
        sidebar_width = document.querySelector(".sidebar_area").offsetWidth;
        calendar_width = calendar_area.offsetWidth;
        console.log(calendar_width-sidebar_width);
        if(sidebar_chk.checked){
            calendar_area.style.width=calendar_width-sidebar_width+"px";
            calendar_area.style.marginLeft=sidebar_width+"px";
        }else{
            calendar_area.style.width="100%";
            calendar_area.style.marginLeft="0%";
        }
    });
});