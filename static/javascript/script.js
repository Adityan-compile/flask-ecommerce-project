if ("serviceWorker" in navigator) {
  navigator.serviceWorker
    .register("serviceWorker.js")
    .then((registration) => {
      console.log("Service worker registered");
      console.log(registration);
    })
    .catch((error) => {
      console.log("Service worker error");
      console.log(error);
    });
}else{
  console.log("Service worker is not working");
}
