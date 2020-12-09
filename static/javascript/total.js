function total(){

    let total = document.getElementById('total').innerHTML

    if(total === 'None'){
        alert('No products in cart')
        window.stop();
    }

}

