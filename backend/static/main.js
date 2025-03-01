// Main Function to Upload Image and Get Prediction
function uploadImage() {
    const fileInput = document.getElementById('imageUpload');
    const file = fileInput.files[0];
    const loading = document.getElementById('loading');
    const prediction = document.getElementById('prediction');
    const benefit = document.getElementById('benefit');

    // Check if a file is selected
    if (!file) {
        alert('Please select an image to upload.');
        return;
    }

    // Check network status
    if (!navigator.onLine) {
        alert('You are offline. Please check your internet connection.');
        return;
    }

    // Show Loading Animation
    loading.style.display = 'block';
    prediction.innerHTML = '';
    benefit.innerHTML = '';

    // Prepare FormData for Upload
    const formData = new FormData();
    formData.append('file', file);

    // Send Image to Flask Backend for Prediction
    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Hide Loading Animation
        loading.style.display = 'none';

        if (data.error) {
            prediction.innerHTML = `⚠️ ${data.error}`;
        } else {
            prediction.innerHTML = `🌿 Herb: ${data.herb}`;
            benefit.innerHTML = `💚 Benefits: ${data.benefit}`;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        loading.style.display = 'none';
        prediction.innerHTML = '❌ Prediction failed. Please try again.';
    });
}

// Event Listener for Network Status Change
window.addEventListener('online', () => {
    alert('You are back online!');
});
window.addEventListener('offline', () => {
    alert('You are offline. Some features may not work.');
});
