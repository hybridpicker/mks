function openNav() {
  if (window.innerWidth < 500) {
    document.getElementById("mks-nav-mobile-menu").style.width = "95%";
    document.getElementById("menuIcon").style.visibility = "hidden";
    document.getElementById("closeMobileMenu").style.display = "flex";
  }
  else{
    document.getElementById("mks-nav-mobile-menu").style.width = "25rem";
    document.getElementById("menuIcon").style.visibility = "hidden";
    document.getElementById("closeMobileMenu").style.display = "flex";
  }
}

function closeNav() {
  document.getElementById("mks-nav-mobile-menu").style.width = "0%";
  document.getElementById("menuIcon").style.visibility = "visible";
  document.getElementById("closeMobileMenu").style.display = "none";
}

// RELOADS WEBPAGE WHEN MOBILE ORIENTATION CHANGES
window.onorientationchange = function() {
  var orientation = window.orientation;
  switch(orientation) {
    case 0:
    case 90:
    case -90: window.location.reload();
    break; }
};
