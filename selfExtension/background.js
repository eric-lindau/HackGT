chrome.runtime.onInstalled.addListener(() => {
	chrome.storage.sync.set({color: '#3aa757'}, () => {
  		console.log("The color is green.");
  	});
  	
});

// chrome.tabs.onCreated.addListener(function(tab) {
//    chrome.tabs.query({'active': true}, function(tab) {
//   		alert(new URL(tab[0].url).hostname);
//   		// Sending a receiving data in JSON format using GET method 
//   		var sites = []
//   		var parser = document.createElement('a');
//   		for (i = 0; i < tab.length; i++){
//   			parser.href = tab[i];
//   			sites.push(parser.hostname);
//   		}
// 	var xhr = new XMLHttpRequest();
// 	var url = "https://swagv1.azurewebsites.net/api/insertMetadata?" + "pid=1";
// 	xhr.open("POST", url, true);
// 	xhr.setRequestHeader("Content-Type", "application/json");
// 	xhr.setBody(JSON.stringify({"sites": sites}));
// 	xhr.onreadystatechange = function () {
// 	if (xhr.readyState === 4 && xhr.status === 200) {
// 	    var json = JSON.parse(xhr.responseText);
// 	    console.log(json.email + ", " + json.password);
// 	}
// 	};
// 	xhr.send();
//  });
// }); 

var prev_url = "";

chrome.tabs.onActivated.addListener(function(activeInfo) {
  // how to fetch tab url using activeInfo.tabid
  chrome.tabs.get(activeInfo.tabId, function(tab){
	// var sites = [];
	// var parser = document.createElement('a');
	// for (i = 0; i < tab.length; i++){
	// 	parser.href = tab[i];
	// 	sites.push(parser.hostname);
	// }
	// console.log(tab.url);
 //     // Sending a receiving data in JSON format using GET method     
	// var xhr = new XMLHttpRequest();
	// var url = "https://swagv1.azurewebsites.net/api/insertMetadata?" + "pid=1";
	// xhr.open("POST", url, false);
	// xhr.setRequestHeader("Content-Type", "application/json");
	// // xhr.setBody();
	// // xhr.onreadystatechange = function () {
	// // 	if (xhr.readyState === 4 && xhr.status === 200) {
	// // 	    var json = JSON.parse(xhr.responseText);
	// // 	    console.log(json.email + ", " + json.password);
	// // 	}
	// // };
	// xhr.send(JSON.stringify({"site": sites[0]}));
 //  	alert(tab.url);
 	if(prev_url !== tab.url) {
		var xhr = new XMLHttpRequest();
		var url = "https://swagv1.azurewebsites.net/api/insertMetadata?" + "pid=1";
		xhr.open("POST", url, false);
		xhr.setRequestHeader("Content-Type", "application/json");
		xhr.send(JSON.stringify({"site": tab.url}));
		prev_url = tab.url;
	}
  });
}); 

chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
	if(prev_url !== tab.url) {
		var xhr = new XMLHttpRequest();
		var url = "https://swagv1.azurewebsites.net/api/insertMetadata?" + "pid=1";
		xhr.open("POST", url, false);
		xhr.setRequestHeader("Content-Type", "application/json");
		xhr.send(JSON.stringify({"site": tab.url}));
		prev_url = tab.url;
	}
});