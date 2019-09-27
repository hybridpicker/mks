function openNav() {
  document.getElementById("blessondNavMobileMenu").style.width = "70%";
  document.getElementById("menuIcon").style.visibility = "hidden";
  document.getElementById("closeMobileMenu").style.display = "flex";
}

function closeNav() {
  document.getElementById("blessondNavMobileMenu").style.width = "0%";
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
