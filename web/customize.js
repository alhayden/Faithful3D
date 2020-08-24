
selected = [1, 0, 1, 0, 1, 1, 1, 1, 0, 1]

function dothing() {}

function mouseover(id) {
	element = document.getElementById(id);
	element.src = element.src.slice(0, -5) + "1.png";
};
function mouseoff(id) {
	element = document.getElementById(id);
	element.src = element.src.slice(0, -5) + "0.png";
}
function toggle(id, index) {
	element = document.getElementById(id);
	if (selected[index] === 1) {
		selected[index] = 0;
		element.src = "images/3dbutton-off-1.png";
	}
	else if (selected[index] === 0) {
		selected[index] = 1;
		element.src = "images/3dbutton-on-1.png";
	}
}
function download() {
	n = 0
	for (x = 0; x < 10; x++) {
		if (selected[x] == 1)
			n += Math.pow(2, x);
	}
	console.log(n);
	window.location.href= "cdn/Faithful3D-1.0.1-custom-" + n + ".zip"
}
