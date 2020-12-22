function validate() {
  let pass = document.getElementById("newPassword").value;
  let cpass = document.getElementById("confirmPass").value;

  if (pass === cpass) {
  } else {
    alert("The entered passwords does not match");
    window.stop();
  }
}
