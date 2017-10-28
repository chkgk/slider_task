function set_touched(event) {
    var hidden_field_id = this.id.substring(0, this.id.length-7) + "touched";
    var touch_element = document.getElementById(hidden_field_id);
    touch_element.value = "True";
    this.removeEventListener('change', set_touched)
}

var sliders = document.getElementsByClassName("slider");
for (i = 0; i < sliders.length; i++) {
    sliders[i].addEventListener('change', set_touched);
}