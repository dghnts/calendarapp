window.addEventListener('load', function (){
    const permission_form_add   = document.querySelector('#permission_form_add');
    const permission_form_area  = document.querySelector('#permission_form_area');

    permission_form_add.addEventListener("click", () => {
        console.log("add");

        const permission_form_init_area = document.querySelector("#permission_form_init_area").children[0].cloneNode(true);
        permission_form_area.appendChild(permission_form_init_area);
    })
});