window.addEventListener('DOMContentLoaded',()=> {
    const search_select = document.querySelector('#search_types'),
        search_name = document.querySelector('#search_name'),
        search_surname = document.querySelector('#search_surname'),
        search_username = document.querySelector('#search_username');

    function forSelect(select,form1,form2,form3) {
        select.addEventListener('click',()=>{
            if (select.value ==="Выберите тип поиска"){
                form1.style.display = "none";
                form2.style.display = "none";
                form3.style.display = "none";
            }else if(select.value === "Поиск по имени"){
                form1.style.display = "block";
                form2.style.display = "none";
                form3.style.display = "none";
            }else if(select.value === "Поиск по фамилии"){
                form1.style.display = "none";
                form2.style.display = "block";
                form3.style.display = "none";
            }else if(select.value === "Поиск по имени пользователя"){
                form1.style.display = "none";
                form2.style.display = "none";
                form3.style.display = "block";
            }
        })
    }

    forSelect(search_select, search_name, search_surname, search_username)


})