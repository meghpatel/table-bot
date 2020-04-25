
// function getdata() {
// 	console.log('Function called')
// 	var request = new XMLHttpRequest();
// 	var data;
// 	request.open('GET', 'http://localhost:5000/getdata', true);

// 	request.onload = function() {
// 	  if (this.status >= 200 && this.status < 400) {
// 	    // Success!
// 	    data = JSON.parse(this.response);
// 	    console.log(data.ans)
// 	    document.getElementById('newtable').innerHTML = data.ans;
// 	  } else {
// 	    // We reached our target server, but it returned an error
// 	    console.log('Server Error')
// 	  }
// 	};

// 	request.onerror = function() {
// 	  // There was a connection error of some sort
// 	  console.log('Connection Error')
// 	};

// 	request.send();

// 	// divID.innerHTML("Table will be added here");
// }


// function submit_data()
// {
// 	const url = `${window.origin}/upload`;
// 	console.log(url);
// 	const form = document.querySelector('form');

// 	const files = document.querySelector('[type=file]').files;
// 	const formData = new FormData();
// 	console.log(formData);
// 	console.log(files);

// 	for (let i = 0; i < files.length; i++) {
// 		let file = files[i];
// 		console.log('file',file);
// 		formData.append('files[]', file);
// 	}

// 	console.log(formData);
// 	console.log("Sending Request");

// 	fetch(url, {
// 			method: "POST",
// 			credentials: "include",
// 			body: formData,
// 			cache: "no-cache",
// 			headers: new Headers({
// 			"content-type": "application/json"
// 			})
// 		}).then(response => {
// 		console.log(response)
// 	})
// }

document.querySelector('#fileUpload').addEventListener('change', event => {
	handleUpload(event)
})

const handleUpload = event => {
	const url = `${window.origin}/upload`;
	console.log(url);

	const files = event.target.files
	// var form = document.querySelector('form');
	const formData = new FormData()
	console.log('file',files);
	formData.append('table', files[0], files[0].name)
	console.log('formdata',formData)

	fetch(url, {
		method: 'POST',
		body: formData
	}).then(response => response.json())
	.then(data => {
		console.log(data)
	})
	.catch(error => {
	console.error(error)
	})
}