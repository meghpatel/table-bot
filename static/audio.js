URL = window.URL || window.webkitURL;
var gumStream;
var rec;
var input;

var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext 

var recordButton = document.getElementById("recordButton");
var stopButton = document.getElementById("stopButton");

recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);

function startRecording() {
	console.log("recordButton clicked");
	stopButton.classList = 'btn btn-primary';
	recordButton.classList = 'hidden';
	var constraints = { audio: true, video:false }

	navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
			console.log("getUserMedia() success, stream created, initializing Recorder.js ...");
			audioContext = new AudioContext();

			
			gumStream = stream;
			input = audioContext.createMediaStreamSource(stream);

			rec = new Recorder(input,{numChannels:2})
			rec.record()
			console.log("Recording started");

		}).catch(function(err) {
			console.log(err);
	});
}

function stopRecording() {
	console.log("stopButton clicked");
	rec.stop();
	gumStream.getAudioTracks()[0].stop();
	recordButton.classList = 'btn btn-primary';
	stopButton.classList = 'hidden';
	rec.exportWAV(createDownloadLink);
}



function createDownloadLink(blob) {
	
	var url = URL.createObjectURL(blob);
	var filename = "12";
	var xhr=new XMLHttpRequest();

	xhr.onload=function(e) {
		if(this.readyState === 4) {
			console.log(e.target.responseText);
			var str = e.target.responseText;
			var response = JSON.parse(str);
			const answer = document.getElementById('response');
			answer.textContent = response.query;
		}
	};

	var fd=new FormData();
	fd.append("audio_data",blob, "2.wav");
	xhr.open("POST","/speech");
	xhr.send(fd);
}