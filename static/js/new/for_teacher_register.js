// register and login functions
window.addEventListener('DOMContentLoaded',()=> {
    const checkbox = document.querySelector('.checkbox'),
        password = document.querySelectorAll('input[type="password"]'),
        subject1 = document.getElementById('fan1'),
        subject2 = document.getElementById('fan2'),
        subject3 = document.getElementById('fan3'),
        buttons = document.querySelectorAll('button'),
        submit = document.querySelector('#submit'),
        radios = document.querySelectorAll('.radios'),
        username = document.querySelectorAll('.username'),
        username2 = document.querySelectorAll('.username2'),
        input_username = document.querySelector('.user_name'),
        flash1 = document.querySelector('#flash1'),
        error_button1 = document.querySelector('#error_button1'),
        flash2 = document.querySelector('#flash2'),
        error_button2 = document.querySelector('#error_button2'),
        password1 = document.querySelector('#password1'),
        password2 = document.querySelector('#password2'),
        xojakent = document.getElementById('xojakent'),
        gazalkent = document.getElementById('gazalkent'),
        chirchiq = document.getElementById('chirchiq');
    let location_input = document.querySelector('.location_input');
    xojakent.addEventListener('click',()=>{
        location_input.value = "xojakent"
        console.log(location_input.value)
    })
    gazalkent.addEventListener('click',()=>{
        location_input.value = "gazalkent"
        console.log(location_input.value)
    })
    chirchiq.addEventListener('click',()=>{
        location_input.value = "chirchiq"
        console.log(location_input.value)
    })

    function usernameError() {
        setTimeout(extra,4000)
        function extra() {
            flash1.style.display = "flex"
            document.documentElement.scrollTop = 0;
            disabled_submit()
            error_button1.addEventListener('click', () => {
                flash1.style.display = 'none'
                input_username.value = ""
                not_disabled()
            })
        }
    }

    function check_user_valid(){
        username.forEach(all_username=>{
            if(input_username.value.toUpperCase()===all_username.innerHTML){
                console.log(input_username.value.toUpperCase()===all_username.innerHTML)
                usernameError()
            }
        })
         username2.forEach(all_username=>{
            if(input_username.value.toUpperCase()===all_username.innerHTML){
                console.log(input_username.value.toUpperCase()===all_username.innerHTML)
                usernameError()
            }
        })
    }

    input_username.addEventListener('keyup',check_user_valid)
    // input_username.addEventListener('keydown',(event)=>{
    //     username.forEach(all_username=>{
    //         if (event.code === "Tab" && input_username.value.toUpperCase()===all_username.innerHTML){
    //             console.log(input_username.value.toUpperCase()===all_username.innerHTML)
    //            usernameError()
    //         }
    //
    //     })
    //     username2.forEach(all_username=>{
    //         if(input_username.value.toUpperCase()===all_username.innerHTML){
    //             console.log(input_username.value.toUpperCase()===all_username.innerHTML)
    //             usernameError()
    //         }
    //     })
    //
    // })

    function checkPassword() {
        if (password1.value !== password2.value){
            flash2.style.display = "flex"
            disabled_submit()
            document.documentElement.scrollTop = 0;
            error_button2.addEventListener('click',()=>{
                password1.value = ""
                password2.value = ""
                flash2.style.display = "none"
                not_disabled()
            })
        }
    }

    function disabled_submit() {
        submit.disabled = true;
        submit.style.cursor = "not-allowed"
    }
    function not_disabled() {
        submit.disabled = false
        submit.style.cursor = "pointer"
    }
    function showPassword() {
        checkbox.addEventListener('click', (event) => {
            password.forEach(pass => {
                if (pass.type === "password") {
                    pass.type = "text";
                } else {
                    pass.type = "password";
                }
            })
        })
    }
    function showSubjects() {
        buttons.forEach(button => {
            button.addEventListener('click', (event) => {
                event.preventDefault()
            })
        })
        radios.forEach(radio => {
            radio.addEventListener('click', () => {
                checkPassword()
                subject1.style.display = "inline";
                if (subject1.value === "Birinchi fan") {
                    disabled_submit()
                }
                subject1.addEventListener('click', () => {
                    if (subject1.value !== "Birinchi fan") {
                        not_disabled()
                    } else {
                        disabled_submit()
                    }
                })
            });
        });
    }

    submit.addEventListener('click',()=>{
        if (subject2.value === "Ikkinchi Fan(Ixtiyoriy)" || subject3.value === "Uchinchi Fan(Ixtiyoriy)"){
            subject2.value = ""
            subject3.value = ""
        }
    })
    showPassword()
    showSubjects()

    const title = document.querySelector('.title'),
        for_date = document.querySelector('.for_date'),
        show_password = document.querySelector('.show_password');
    if (title.innerHTML.length === 19){
        for_date.style.marginLeft = "40px";
        show_password.style.marginLeft = "43px";
    }
})

