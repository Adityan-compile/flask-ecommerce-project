function validate (){
    var password = document.getElementById("Password").value;
    var confirmPassword = document.getElementById("confirmPassword");
    
    if (password==confirmPassword) {
        console.log("Passwords confirmed");
    }else{
        alert("Passwords does not match");
        window.stop();
    }
}