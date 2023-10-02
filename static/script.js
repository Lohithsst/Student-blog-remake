function opennav(id) {
    var x = document.getElementById(id);
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}

document.addEventListener('click', function(event) {
    var buttons = document.getElementById('Aboutbutton');
    var isClickInside = buttons.contains(event.target);
    var text = document.getElementById('Abouttext');

    if (!isClickInside && text.style.display === "flex") {
      text.style.display = "none";
    }
});

document.addEventListener('click', function(event) {
  var buttons = document.getElementById('Resourcesbutton');
  var isClickInside = buttons.contains(event.target);
  var text = document.getElementById('Resourcestext');

  if (!isClickInside && text.style.display === "flex") {
    text.style.display = "none";
  }
});

document.addEventListener('click', function(event) {
  var buttons = document.getElementById('Housesbutton');
  var isClickInside = buttons.contains(event.target);
  var text = document.getElementById('Housestext');

  if (!isClickInside && text.style.display === "flex") {
    text.style.display = "none";
  }
});