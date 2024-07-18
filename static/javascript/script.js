document.addEventListener('DOMContentLoaded', ()=> {
    let count = 0;
    const counterDisplay = document.getElementById('counter');
    const button = document.getElementById('incrementButton');

    button.addEventListener('click', function() {
        count++;
        counterDisplay.textContent = count;
    });
});