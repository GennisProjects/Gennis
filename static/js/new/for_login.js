    const checkbox = document.querySelector('.checkbox'),
        password = document.querySelectorAll('input[type="password"]');
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
    showPassword()