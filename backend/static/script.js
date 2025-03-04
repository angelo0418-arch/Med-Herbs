document.addEventListener("DOMContentLoaded", function() {
    function handleImageUpload() {
        const fileInput = document.getElementById('imageUpload');
        const file = fileInput?.files[0]; // Optional chaining to prevent errors
        const loading = document.getElementById('loading');
        const prediction = document.getElementById('prediction');
        const benefit = document.getElementById('benefit');
        const imagePreview = document.getElementById('imagePreview');

        if (!fileInput || !loading || !prediction || !benefit || !imagePreview) {
            console.error("❌ One or more elements are missing in the DOM.");
            return;
        }

        if (!file) {
            alert('Please select an image to upload.');
            return;
        }

        // Display uploaded image preview
        const reader = new FileReader();
        reader.onload = function(event) {
            imagePreview.src = event.target.result;
            imagePreview.style.display = 'block';
        };
        reader.readAsDataURL(file);

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
        const loadingDuration = (effectiveType === '4g' || !effectiveType) ? 1000 : 3000;

        // Prepare FormData for Upload
        const formData = new FormData();
        formData.append('file', file);

        setTimeout(() => {
            fetch('http://127.0.0.1:5000/predict', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                loading.style.display = 'none';

                if (data.error) {
                    prediction.innerHTML = `❌ Error: ${data.error}`;
                } else if (data.warning) {
                    prediction.innerHTML = `⚠️ Warning: ${data.warning}`;
                } else {
                    prediction.innerHTML = `🌿 Herb: <strong>${data.herb}</strong>`;
                    benefit.innerHTML = `💚 Benefits: <strong>${data.benefit}</strong>`;
                }
            })
            .catch(error => {
                loading.style.display = 'none';
                prediction.innerHTML = '❌ Prediction failed. Please try again.';
                console.error("Error fetching prediction:", error);
            });
        }, loadingDuration);
    }

    // Attach event listener once HTML is fully loaded
    const fileInput = document.getElementById('imageUpload');
    if (fileInput) {
        fileInput.addEventListener('change', handleImageUpload);
        console.log("✅ Event listener added to #imageUpload");
    } else {
        console.error("❌ Element #imageUpload not found in DOM!");
    }
});
