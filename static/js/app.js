var full_url = location.href;
var url = location.protocol + '//' + location.host + location.pathname;
var mainMenuLinks = document.getElementById("mainMenu").getElementsByTagName("a");
var sideMenuLinks = document.getElementById("sidebarMenu").getElementsByTagName("a");
for(var i=0; i<mainMenuLinks.length; i++) {
  var lb = mainMenuLinks[i].href;
  if(lb == url || lb == full_url) {
    mainMenuLinks[i].className += " active";
  }
}
for(var i=0; i<sideMenuLinks.length; i++) {
  var lb = sideMenuLinks[i].href;
  if(lb == url || lb == full_url) {
    sideMenuLinks[i].className += " active";
  }
}    