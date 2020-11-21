function stock() {
    var x = document.getElementById('stockstatus');

    if (x === "Out of Stock") {
        x.classList.add('disabled')
        document.getElementById('stockstatus').createAttribute('disabled');
    }else{
        x.classList.remove('disabled')
        document.getElementById('stockstatus').removeAttribute('disabled');
    }
}