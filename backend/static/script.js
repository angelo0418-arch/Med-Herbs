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

                if (data.error || data.warning) {
                    prediction.innerHTML = '❌ Prediction failed. Please try again.';
                } else {
                    prediction.innerHTML = `🌿 <strong>Herb</strong>: ${data.herb}`;
                    benefit.innerHTML = `💚 <strong>Benefits</strong>: ${data.benefit}`;
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

 
function showContent(sectionId) {
    // Itago lahat ng sections
    document.querySelectorAll('.content, .main-wrapper, .form-container').forEach(section => {
        section.classList.add('d-none');
    });

    // Ipakita lang ang napiling section
    let section = document.getElementById(sectionId);
    if (section) {
        section.classList.remove('d-none');
    }

    // Disable scrolling kapag nasa login o sign-up form
    if (sectionId === 'login-form' || sectionId === 'signup-form') {
        document.body.style.overflow = 'hidden'; // Disable scroll
    } else {
        document.body.style.overflow = 'auto'; // Enable scroll kapag bumalik sa ibang section
    }
}


function closeOffcanvas() {
    var offcanvas = document.getElementById('offcanvasNavbar');
    var bsOffcanvas = bootstrap.Offcanvas.getInstance(offcanvas);
    if (bsOffcanvas) {
        bsOffcanvas.hide();
    }
}

