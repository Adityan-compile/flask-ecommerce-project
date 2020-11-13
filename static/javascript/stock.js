function stock() {
    var x = document.getElementById('stockstatus');

    if (x = "Out of stock") {
        document.getElementById('stockstatus').setAttribute("aria-disabled", "true");
    } else {
        document.getElementById('stockstatus').setAttribute("aria-disabled", "false");
    }
}