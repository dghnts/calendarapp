window.addEventListener('load', function (){
    const permission_form_add   = document.querySelector('#permission_form_add');
    const permission_form_area  = document.querySelector('#permission_form_area');
    const authority = [
        { value: "3", read: true, write: true, chat: true},
        { value: "0", read: true, write: false, chat: false},
        { value: "1", read: true, write: true, chat: false},
        { value: "2", read: true, write: false, chat: true},
    ];
    console.log(permission_form_add);
    permission_form_add.addEventListener("click", () => {
        addPermissionForm(permission_form_area, authority); 
    });
});