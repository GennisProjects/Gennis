window.addEventListener('DOMContentLoaded', () => {


    const menu = document.querySelector('.nav_menu'),
    menuItem = document.querySelectorAll('.menu_item'),
    basic = document.querySelector('.basic'),
    hamburger = document.querySelector('.hamburger');

    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('hamburger_active');
        menu.classList.toggle('nav_menu_active');
        basic.classList.toggle('basic_active');
    });

    menuItem.forEach(item => {
        item.addEventListener('click', () => {
            hamburger.classList.toggle('hamburger_active');
            menu.classList.toggle('nav_menu_active');
        })
    })
    const change_photo = document.querySelector('.image_upload'),
        upload = document.querySelector('.upload_img'),
        ready_photo = document.querySelector('.ready_photo');

    change_photo.addEventListener('mouseleave',()=>{
        if (upload.value !== ""){
            ready_photo.style.display = "flex";
            console.log('hello1')
        }else {
            ready_photo.style.display = "none";
            console.log('hello2')
        }
     });


    $('[data-user=user-profile]').on('click', function () {
        $('.overlay, [data-modal=user-profile]').fadeIn();
    });

    $('#change_profile').on('click', function () {
        $('.overlay-password, [data-modal=user-password]').fadeIn();
    });

    $('.modal__close').on('click', function () {
        $('.overlay, [data-modal=user-profile]').fadeOut();
    });

    $('.modal-password__close_2').on('click', function () {
        $('.overlay-password, [data-modal=user-password]').fadeOut();
    });



    const overlay = document.querySelector('.overlay'),
        overlay_password = document.querySelector('.overlay-password');

    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) {
            overlay.style.display = 'none'
        }
    })
    overlay_password.addEventListener('click', (e) => {
        if (e.target === overlay_password) {
            overlay_password.style.display = 'none'
        }
    })

    $(
        function () {
            let location = false
            $("#new_student_location_list").hide();
            $("#location_list").click(function () {
                if (location === false){
                    $("#new_student_location_list").slideDown(50)
                    location = !location
                    $("#new_student_location_list_down").toggleClass('menu_item_li_down_array_active')
                }else {
                    $("#new_student_location_list").slideUp(50)
                    location = !location
                    $("#new_student_location_list_down").toggleClass('menu_item_li_down_array_active')
                }
            })
        }
    )
     $(
        function () {
            location2 = false
            $("#new_student_location_list_2").hide();
            $("#location_list_2").click(function () {
                if (location2 === false){
                    $("#new_student_location_list_2").slideDown(50)
                    location2 = !location2
                    $("#new_student_location_list_down_2").toggleClass('menu_item_li_down_array_active')
                }else {
                    $("#new_student_location_list_2").slideUp(50)
                    location2 = !location2
                    $("#new_student_location_list_down_2").toggleClass('menu_item_li_down_array_active')
                }
            })

        }
    )
     $(
        function () {
            let location3 = false
            $("#new_student_location_list_3").hide();
            $("#location_list_3").click(function () {
                if (location3 === false){
                    $("#new_student_location_list_3").slideDown(50)
                    location3 = !location3
                    $("#new_student_location_list_down_3").toggleClass('menu_item_li_down_array_active')
                }else {
                    $("#new_student_location_list_3").slideUp(50)
                    location3 = !location3
                    $("#new_student_location_list_down_3").toggleClass('menu_item_li_down_array_active')
                }
            })
        }
    )
     $(
        function () {
            let location4 = false
            $("#new_student_location_list_4").hide();
            $("#location_list_4").click(function () {
                if (location4 === false){
                    $("#new_student_location_list_4").slideDown(50)
                    location4 = !location4
                    $("#new_student_location_list_down_4").toggleClass('menu_item_li_down_array_active')
                }else {
                    $("#new_student_location_list_4").slideUp(50)
                    location4 = !location4
                    $("#new_student_location_list_down_4").toggleClass('menu_item_li_down_array_active')
                }
            })
        }
    )
     $(
        function () {
            let location5 = false
            $("#new_student_location_list_5").hide();
            $("#location_list_5").click(function () {
                if (location5 === false){
                    $("#new_student_location_list_5").slideDown(50)
                    location5 = !location5
                    $("#new_student_location_list_down_5").toggleClass('menu_item_li_down_array_active')
                }else {
                    $("#new_student_location_list_5").slideUp(50)
                    location5 = !location5
                    $("#new_student_location_list_down_5").toggleClass('menu_item_li_down_array_active')
                }
            })

        }
    )

})