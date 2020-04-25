
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
	const url1 = `${window.origin}/getanswer`;
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
		// html = JSON.parse(data);
// 	    console.log(data.ans)
	    document.getElementById('tabledis').innerHTML = data.ans;
	    const box = document.getElementById('chat1');
	    const inp = document.createElement("INPUT");
	    inp.setAttribute('type','text');
	    inp.setAttribute('size',50);
	    inp.setAttribute('id','inputbox')
	    box.appendChild(inp);
	    box.style['text-align'] = 'center';
	    inp.addEventListener("keyup", function(event) {
			if (event.keyCode === 13) {
				event.preventDefault();
				console.log("Click");
				// window.alert(inp.value);
				let query = inp.value;
				const response = document.getElementById('response');
				response.innerHTML = query;
				inp.value = ''

				const entry = { query }
				fetch(url1,{
					method:'POST',
					credentials: "include",
					body: JSON.stringify(entry),
					cache: "no-cache",
					headers: new Headers({
						"content-type": "application/json"
    				})
				}).then(response => response.json())
				.then(data => {
					console.log(data)
					// const chatbox = document.getElementById('chatbox')
					const reply = document.createElement('div')
					response.appendChild(reply)
					// console.log(typeof(data))
					// const obj = JSON.parse(data)
					reply.innerHTML = data
					reply.style['text-align'] = "right";
				});
			}
		});
	})
	.catch(error => {
	console.error(error)
	})
}