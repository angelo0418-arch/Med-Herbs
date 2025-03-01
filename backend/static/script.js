// Main Function to Handle Image Upload and Prediction
function handleImageUpload() {
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

    // Adjust loading speed based on network signal
    const connection = navigator.connection || {};
    const effectiveType = connection.effectiveType || '4g';
    const loadingDuration = effectiveType === '4g' ? 1000 : 3000;

    // Prepare FormData for Upload
    const formData = new FormData();
    formData.append('file', file);

    console.log('Starting image upload...');
    console.log('Selected file:', file);

    setTimeout(() => {
        fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            console.log('Response status:', response.status);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Response data:', data);
            loading.style.display = 'none';

            if (data.error) {
                prediction.innerHTML = `⚠️ ${data.error}`;
            } else if (data.warning) {
                prediction.innerHTML = `⚠️ ${data.warning}`;
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
    }, loadingDuration);
}

// Automatic Trigger for Image Upload
document.getElementById('imageUpload').addEventListener('change', handleImageUpload);

// Event Listener for Network Status Change
window.addEventListener('online', () => {
    alert('You are back online!');
});
window.addEventListener('offline', () => {
    alert('You are offline. Some features may not work.');
});
