chrome.runtime.onInstalled.addListener(() => {
	chrome.storage.sync.set({color: '#3aa757'}, () => {
  		console.log("The color is green.");
  	});
  	
});

/*chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
   chrome.tabs.query({'active': true}, function(tab) {
  		alert(tab[0].url);
 });
}); 
*/
chrome.tabs.onCreated.addListener(function(tab) {
   chrome.tabs.query({'active': true}, function(tab) {
  		alert(tab[0].url);
 });
}); 

chrome.tabs.onActivated.addListener(function(activeInfo) {
  // how to fetch tab url using activeInfo.tabid
  chrome.tabs.get(activeInfo.tabId, function(tab){
  	alert(tab.url);
     console.log(tab.url);
  });
}); 
//chrome.extension.getBackgroundPage().console.log('foo');
//https://stackoverflow.com/questions/11156479/how-do-i-use-chrome-tabs-onupdated-addlistener