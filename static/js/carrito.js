var updateBtns = document.getElementsByClassName('update-carrito')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productoId = this.dataset.producto
		var action = this.dataset.action
		console.log('productoId:', productoId, 'Action:', action)
		console.log('USER:', user)

		if (user == 'AnonymousUser'){
			console.log('User is not authenticated')

		}else{
			updateUserPedido(productoId, action)
		}
	})
}

function updateUserPedido(productoId, action){
	var url = '/update_item/'
	console.log('URL:', url)
    fetch(url, {
		method:'POST',
		headers:{
			'Content-Type':'application/json',
			'X-CSRFToken' :csrftoken,
		},
		body:JSON.stringify({'productoId':productoId, 'action':action})
	})
	 .then((response) => {
		 return response.json();
	})
	 .then((data) => {
		 location.reload()
	});