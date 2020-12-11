function validate() {
  let pass = document.getElementById("newPassword").value;
  let cpass = document.getElementById("confirmPass").value;

  if (pass === cpass) {
    return true;
  } else {
    alert("The entered passwords does not match");
    window.stop();
    return false;
  }
}
