function validate (){
    var password = document.getElementById("password").value;
    var confirmPassword = document.getElementById("confirm-password");
    
    if (password==confirmpassword) {
        console.log("passwords confirmed")
    }else{
        alert("Passwords does not match");
        window.stop();
    }
}