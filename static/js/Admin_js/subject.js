window.addEventListener('DOMContentLoaded', () => {
    const subjects = document.querySelector('#subjects'),
        list_students_item_comment = document.querySelectorAll('.list_students_item_comment'),
        all_students_xojakent = document.querySelector("#all_students_xojakent"),
        xojakent_english = document.querySelector('#xojakent_english'),
        xojakent_russian = document.querySelector('#xojakent_russian'),
        xojakent_math = document.querySelector("#xojakent_math"),
        xojakent_history = document.querySelector("#xojakent_history"),
        xojakent_tongue = document.querySelector('#xojakent_tongue'),
        xojakent_chemistry = document.querySelector('#xojakent_chemistry');


    function showSubject(list_subject,sub1,sub2,sub3,sub4,sub5,sub6,sub7) {
        list_subject.addEventListener('click',()=>{
            if (list_subject.value === "Все студенты"){
                showBorder()
                sub1.hidden = false;
                sub2.hidden = true;
                sub3.hidden = true;
                sub4.hidden = true;
                sub5.hidden = true;
                sub6.hidden = true;
                sub7.hidden = true;
            }else if (list_subject.value === "Ingliz tili"){
                hideBorder()
                sub1.hidden = true;
                sub2.hidden = false;
                sub3.hidden = true;
                sub4.hidden = true;
                sub5.hidden = true;
                sub6.hidden = true;
                sub7.hidden = true;
            }else if (list_subject.value === "Rus tili"){
                hideBorder()
                sub1.hidden = true;
                sub2.hidden = true;
                sub2.hidden = false;
                sub4.hidden = true;
                sub5.hidden = true;
                sub6.hidden = true;
                sub7.hidden = true;
            }else if(list_subject.value === "Matematika"){
                hideBorder()
                sub1.hidden = true;
                sub2.hidden = true;
                sub2.hidden = true;
                sub4.hidden = false;
                sub5.hidden = true;
                sub6.hidden = true;
                sub7.hidden = true;
            }else if (list_subject.value === "Tarix"){
                hideBorder()
                sub1.hidden = true;
                sub2.hidden = true;
                sub2.hidden = true;
                sub4.hidden = true;
                sub5.hidden = false;
                sub6.hidden = true;
                sub7.hidden = true;
            }else if (list_subject.value === "Ona tili va Adabiyot"){
                hideBorder()
                sub1.hidden = true;
                sub2.hidden = true;
                sub2.hidden = true;
                sub4.hidden = true;
                sub5.hidden = true;
                sub6.hidden = false;
                sub7.hidden = true;
            }else if (list_subject.value === "Kimyo"){
                hideBorder()
                sub1.hidden = true;
                sub2.hidden = true;
                sub2.hidden = true;
                sub4.hidden = true;
                sub5.hidden = true;
                sub6.hidden = true;
                sub7.hidden = false;
            }
        })
    }
    function hideBorder(){
        list_students_item_comment.forEach(border=>{
            border.style.borderRight = "none"
        })
    }
    function showBorder(){
        list_students_item_comment.forEach(border=>{
            border.style.borderRight = "1px solid"
        })
    }
    showSubject(subjects,all_students_xojakent,xojakent_english,xojakent_russian,
        xojakent_math,xojakent_history,xojakent_tongue,xojakent_chemistry)
})