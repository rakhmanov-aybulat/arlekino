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


const captchaForm = document.getElementById('captcha-form');
captchaForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const imageFile = inputFile.files[0];
    const objectsToDetect = document.getElementById('objects-to-detect').value;
    
    const base64Image = await new Promise((resolve) => {
        const reader = new FileReader();
        reader.onloadend = () => resolve(reader.result.split(',')[1]);
        reader.readAsDataURL(imageFile);
    });
    
    const response = await fetch('/solve/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': '{{ csrf_token }}',
        },
        body: new URLSearchParams({
          image: base64Image,
          objects: objectsToDetect,
        }),
    });
    
    const data = await response.json();

    imageView.style.backgroundImage = `url(data:image/png;base64,${data.image})`;
    imageView.textContent = "";
    imageView.style.border = 0;
    const title = document.getElementById("title");
    title.textContent = `Objects Found: ${data.objectsCount}`
});

