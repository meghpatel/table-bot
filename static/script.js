
function getdata() {
	console.log('Function called')
	var request = new XMLHttpRequest();
	var data;
	request.open('GET', 'http://localhost:5000/getdata', true);

	request.onload = function() {
	  if (this.status >= 200 && this.status < 400) {
	    // Success!
	    data = JSON.parse(this.response);
	    console.log(data.ans)
	    document.getElementById('newtable').innerHTML = data.ans;
	  } else {
	    // We reached our target server, but it returned an error
	    console.log('Server Error')
	  }
	};

	request.onerror = function() {
	  // There was a connection error of some sort
	  console.log('Connection Error')
	};

	request.send();

	// divID.innerHTML("Table will be added here");
}