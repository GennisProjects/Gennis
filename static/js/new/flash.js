const close_flash = document.querySelector('.close_flash'),
        for_flash = document.querySelector('.for_flash');
if(close_flash) {
    close_flash.addEventListener('click', () => {
        for_flash.style.display = "none";
    });
}




const close = document.querySelector('#close'),
        flash = document.querySelector('.flash');
if(close) {
    close.addEventListener('click', () => {
        flash.style.display = "none";
    });
}
