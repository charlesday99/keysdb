//Site-wide resizing
function mobileWidthCheck() {
	//Width of the orange left border
	const BAR_WIDTH = 6;
	
	//Checks whether the window is less then 900 pixels
	if (window.innerWidth < 900) {
		
		//Checks whether the scroll bar is visible
		if (scrollbarVisible(document.body)) {
			document.getElementById("main").style.setProperty('width', (document.body.clientWidth - BAR_WIDTH) + "px");
		} else {
			document.getElementById("main").style.setProperty('width', (window.innerWidth - BAR_WIDTH) + "px");
		}
		
	} else {
		document.getElementById("main").style.setProperty('width', "70%");
	}
}

//Returns boolean for whether the scroll bar is visible
function scrollbarVisible(element) {
	return element.scrollHeight > element.clientHeight;
}

//Register the worker after load and print any errors
function addWorker() {
	if ('serviceWorker' in navigator) {
		window.addEventListener('load', function() {
			navigator.serviceWorker.register('worker.js')
			.then(function(registration) {
				console.log('Registration successful, scope is:', registration.scope);
			})
			.catch(function(error) {
				console.log('Service worker registration failed, error:', error);
			});
		});
	}
}

//Create a cookie with the given key, value and expiry length
function setCookie(cname, cvalue, exdays) {
	var d = new Date();
	d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
	var expires = "expires="+d.toUTCString();
	document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

//Get a cookie with the given key
function getCookie(cname) {
	var name = cname + "=";
	var ca = document.cookie.split(';');
	for(var i = 0; i < ca.length; i++) {
		var c = ca[i];
		while (c.charAt(0) == ' ') {
			c = c.substring(1);
		}
		
		if (c.indexOf(name) == 0) {
			return c.substring(name.length, c.length);
		}
	}
	return "";
}