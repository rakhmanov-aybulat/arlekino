const dropArea = document.getElementById("drop-area");
const inputFile = document.getElementById("input-file");
const imageView = document.getElementById("image-view");

function uploadImage(event) {
	let imageLink = URL.createObjectURL(inputFile.files[0]);
	imageView.style.backgroundImage = `url(${imageLink})`;
    imageView.textContent = "";
    imageView.style.border = 0;
}

inputFile.addEventListener("change", uploadImage);

dropArea.addEventListener("dragover", (event) => {
    event.preventDefault();
})
dropArea.addEventListener("drop", (event) => {
    event.preventDefault();
    inputFile.files = event.dataTransfer.files;
    uploadImage();
})

