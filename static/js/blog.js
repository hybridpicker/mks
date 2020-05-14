var countImg = document.getElementById("blogContent").getElementsByTagName("img").length
function createGallery(countImg){
  // Creating for every Img an ID and className
  for (i = 0; i < countImg; i++) {
      document.getElementById("blogContent").getElementsByTagName("img")[i].setAttribute("id", "blogImg" + i);
      document.getElementById("blogContent").getElementsByTagName("img")[i].setAttribute("class", "blogImg");
      var img = document.getElementById("blogImg" + i);
      // Check if landscape or Portrait
      var width = document.getElementById("blogImg" + i).width;
      var height = document.getElementById("blogImg" + i).height;
      if ( height > width ){
        img.classList.add("portrait");
      }
      else {
        img.classList.add("landscape");
      }
      img.removeAttribute("style");
  }
  // Find paragraphs that contains an Image
  var paragraphCount = document.querySelectorAll("p").length
  for (i = 0; i < paragraphCount; i++) {
      if (document.querySelectorAll("p")[i].contains(document.querySelector(".blogImg"))){
        document.querySelectorAll("p")[i].setAttribute("class", "gallery-show");
      }
  }

}

createGallery(countImg);
