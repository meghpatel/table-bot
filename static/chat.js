console.log("I am here");
document.querySelector('#inputbox').addEventListener('keyup', event => {
	chat(event)
});

const chat = event => {
	const url1 = `${window.origin}/getanswer`;

	var pageHeight = $('#chatbot').height();

	if (event.keyCode === 13) {
		event.preventDefault();
		console.log("Click");

		inp = document.querySelector('#inputbox');
		let query = inp.value;

		//Creating a Chatbubble
		const cb = document.getElementById('chatbot');
		const que = document.createElement('div');
		que.className = "talk-bubble tri-right round left-top";
		const que_text = document.createElement('div');
		que_text.className = "talktext";
		const pr = document.createElement('p');
		pr.innerHTML = query;
		que_text.appendChild(pr);
		que.appendChild(que_text);
		cb.appendChild(que);
		cb.appendChild(document.createElement("br"));
		pageHeight = pageHeight + 5000;
  		$('#chatbot').scrollTop(pageHeight);
		// //get container element
		// var container = document.getElementById("splitright");
		// //scroll down
		// container.scrollTop = container.scrollHeight;

		// response.innerHTML = query;
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
			// const reply = document.createElement('div')
			// response.appendChild(reply)
			// console.log(typeof(data))
			// const obj = JSON.parse(data)

			
			//Creating response bubble
			const response_bubble = document.createElement('div');
			response_bubble.className = 'talk-bubble tri-right round right-top' ;
			const resbub_text = document.createElement('div');
			resbub_text.className = 'talktext' ;
			const rp = document.createElement('p');
			rp.innerHTML = data;
			resbub_text.appendChild(rp);
			response_bubble.appendChild(resbub_text);
			cb.appendChild(response_bubble);
			cb.appendChild(document.createElement("br"));
			pageHeight = pageHeight + 5000;
  			$('#chatbot').scrollTop(pageHeight);
			// reply.innerHTML = data
			// reply.style['text-align'] = "right";

			
		});
	}
}