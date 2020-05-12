document.querySelector('#fileUpload').addEventListener('change', event => {
	const files = event.target.files;
	handleUpload(files)
});

let dropArea = document.getElementById('drop-area');

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
	dropArea.addEventListener(eventName, preventDefaults, false)
});

function preventDefaults (e) {
	e.preventDefault()
	e.stopPropagation()
}

;['dragenter', 'dragover'].forEach(eventName => {
	dropArea.addEventListener(eventName, highlight, false)
})

;['dragleave', 'drop'].forEach(eventName => {
	dropArea.addEventListener(eventName, unhighlight, false)
})

function highlight(e) {
	dropArea.classList.add('highlight')
}

function unhighlight(e) {
	dropArea.classList.remove('highlight')
}

dropArea.addEventListener('drop', handleDrop, false)

function handleDrop(e) {
	let dt = e.dataTransfer
	let files = dt.files

	handleUpload(files)
}


const handleUpload = files => {
	const url = `${window.origin}/upload`;
	const url1 = `${window.origin}/getanswer`;
	console.log(url);
	// let files;

	// if (event.target.files){
	// 	files = event.target.files;
	// 	console.log("Inside IFFF;");
	// }
	// else{
	// 	let dt = event.dataTransfer;
	// 	let files_new = dt.files;	
	// 	files = files_new;
	// }

	// console.log(files_new)

	// const files = files_new;
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
	    document.getElementById('tabledis').innerHTML = data.ans;
	    const box = document.getElementById('chat1');
	    const inp = document.getElementById("inputbox");
	    const rec_btn = document.getElementById("recordButton");
	    const upload_box = document.getElementById("drop-area");

	    rec_btn.style.display = "inline";
	    inp.setAttribute('type','text');
	    inp.setAttribute('size',50);
	    inp.style.display = "inline";
	    inp.focus();
	    box.style['text-align'] = 'center';
	    upload_box.style.display = "none";
	  })
	.catch(error => {
	console.error(error)
	})
}