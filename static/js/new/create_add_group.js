const checkbox = document.querySelectorAll('.checkbox');

for (let d = 0; d < checkbox.length; d++) {
    const checked = checkbox[d]
    checked.onchange = function (event) {
        const check_id = event.target.dataset['id']
        const checking = event.target.checked
        console.log(check_id)
        fetch('/chosen_student/' + check_id, {
            method: "POST",
            body: JSON.stringify({
                'completed': checking
            }),
            headers: {
                'Content-type': 'application/json'
            }
        })
    }
}
