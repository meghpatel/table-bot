document.querySelector('#fileUpload').addEventListener('change', event => {
	handleUpload(event)
})

const handleUpload = event => {
	const url = `${window.origin}/upload`;
	const url1 = `${window.origin}/getanswer`;
	console.log(url);

	const files = event.target.files
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

	    rec_btn.style.display = "inline";
	    inp.setAttribute('type','text');
	    inp.setAttribute('size',50);
	    inp.style.display = "inline";
	    inp.focus();
	    box.style['text-align'] = 'center';
	  })
	.catch(error => {
	console.error(error)
	})
}