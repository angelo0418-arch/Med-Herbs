function processImage() {
  const input = document.getElementById("imageInput");
  const file = input.files[0];
  const preview = document.getElementById("preview");
  const loading = document.getElementById("loading");
  const result = document.getElementById("result");

  if (!file) return;

  // Display image preview
  const reader = new FileReader();
  reader.onload = function(e) {
      preview.src = e.target.result;
      preview.style.display = "block";
  };
  reader.readAsDataURL(file);

  // Show loading indicator and clear result
  loading.style.display = "block";
  result.innerText = "";

  // Send image for prediction
  const formData = new FormData();
  formData.append("file", file);

  fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      body: formData
  })
  .then(response => response.json())
  .then(data => {
      loading.style.display = "none";
      result.innerText = "Prediction: " + data.prediction;
  })
  .catch(error => {
      console.error("Error:", error);
      loading.style.display = "none";
      result.innerText = "Error identifying herb.";
  });
}




























































// chatgpt

document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const fileInput = document.getElementById('fileInput');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    const resultDiv = document.getElementById('result');
    const loadingAnimation = document.getElementById('loading');

    // === Show Loading Animation ===
    loadingAnimation.style.display = 'block';
    resultDiv.innerText = '';

    // === Check Network Speed ===
    const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
    let animationDuration = 2000; // Default: 2 seconds

    if (connection) {
        if (connection.effectiveType === '4g') {
            animationDuration = 1000; // Mabilis ang connection
        } else if (connection.effectiveType === '3g' || connection.effectiveType === '2g') {
            animationDuration = 3000; // Mabagal ang connection
        }
    }

    // === Send Image to Backend ===
    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        setTimeout(() => {
            loadingAnimation.style.display = 'none';
            resultDiv.innerText = data.result;
        }, animationDuration);
    })
    .catch(error => {
        console.error('Error:', error);
        loadingAnimation.style.display = 'none';
        resultDiv.innerText = 'Error occurred. Please try again.';
    });
});
