window.addEventListener("load",function(){
    calendar_prev_button=document.querySelector(".fc-prev-button");
    calendar_today_button=document.querySelector(".fc-today-button");
    calendar_next_button=document.querySelector(".fc-next-button");

    list_prev_buttons=document.querySelectorAll(".fc-prev-button");
    list_today_buttons=document.querySelectorAll(".fc-today-button");
    list_next_buttons=document.querySelectorAll(".fc-next-button");
    
    for(var i=1; i<list_next_buttons.length; i++){
        list_prev_buttons[i].style.display    = "none";
        list_today_buttons[i].style.display   = "none";
        list_next_buttons[i].style.display    = "none";    
    }
    
    calendar_prev_button.addEventListener('click', function(){
        for(var i=1; i<list_next_buttons.length; i++){
            list_prev_buttons[i].click();   
        }
    });
    calendar_today_button.addEventListener('click', function(){
        for(var i=1; i<list_next_buttons.length; i++){
            list_today_buttons[i].click();    
        }
    });
    calendar_next_button.addEventListener('click', function(){
        for(var i=1; i<list_next_buttons.length; i++){
            list_next_buttons[i].click();  
        }
    });
    

    calendar_dayGridMonth_button=document.querySelector(".fc-dayGridMonth-button");
    calendar_dayGridWeek_button=document.querySelector(".fc-timeGridWeek-button");
    calendar_dayGridDay_button=document.querySelector(".fc-timeGridDay-button");

    list_listMonth_buttons=document.querySelectorAll(".fc-listMonth-button");
    list_listWeek_buttons=document.querySelectorAll(".fc-listWeek-button");
    list_listDay_buttons=document.querySelectorAll(".fc-listDay-button");

    
    list_listMonth_buttons.forEach(btn => {
        btn.style.display = "none"
    });  
    list_listWeek_buttons.forEach(btn => {
        btn.style.display = "none";
    });
    list_listDay_buttons.forEach(btn => {
        btn.style.display  = "none";
    });
    

    calendar_dayGridMonth_button.addEventListener('click', function(){
        list_listMonth_buttons.forEach(btn => { 
            btn.click();
        });
        //console.log("prev");
    });
    calendar_dayGridWeek_button.addEventListener('click', function(){
        list_listWeek_buttons.forEach(btn => {
            btn.click();
        })
        //console.log("today");
    });
    calendar_dayGridDay_button.addEventListener('click', function(){
        list_listDay_buttons.forEach(btn => {
            btn.click();
        });
    });
});