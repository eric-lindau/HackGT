chrome.runtime.onInstalled.addListener(() => {
	chrome.storage.sync.set({color: '#3aa757'}, () => {
  		console.log("The color is green.");
  	});
  	
});

chrome.tabs.onCreated.addListener(function(tab) {
   chrome.tabs.query({'active': true}, function(tab) {
  		alert(new URL(tab[0].url).hostname);
  		// Sending a receiving data in JSON format using GET method     
	var xhr = new XMLHttpRequest();
	var url = "https://swagv1.azurewebsites.net/api/insertMetadata?" + "pid=1";
	xhr.open("GET", url, true);
	xhr.setRequestHeader("Content-Type", "application/json");
	xhr.setBody(JSON.stringify({"sites": tab}));
	xhr.onreadystatechange = function () {
	if (xhr.readyState === 4 && xhr.status === 200) {
	    var json = JSON.parse(xhr.responseText);
	    console.log(json.email + ", " + json.password);
	}
	};
	xhr.send();
 });
}); 

chrome.tabs.onActivated.addListener(function(activeInfo) {
  // how to fetch tab url using activeInfo.tabid
  chrome.tabs.get(activeInfo.tabId, function(tab){
  	alert(tab.url);
     console.log(tab.url);
     // Sending a receiving data in JSON format using GET method     
	var xhr = new XMLHttpRequest();
	var url = "https://swagv1.azurewebsites.net/api/insertMetadata?" + "pid=1";
	xhr.open("GET", url, true);
	xhr.setRequestHeader("Content-Type", "application/json");
	xhr.setBody(JSON.stringify({"sites": tab}));
	xhr.onreadystatechange = function () {
	if (xhr.readyState === 4 && xhr.status === 200) {
	    var json = JSON.parse(xhr.responseText);
	    console.log(json.email + ", " + json.password);
	}
	};
	xhr.send();
  });
}); 