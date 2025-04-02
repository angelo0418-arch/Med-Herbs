document.addEventListener("DOMContentLoaded", function () {
    function handleImageUpload() {
        const fileInput = document.getElementById('imageUpload');
        const file = fileInput?.files[0]; 
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
        reader.onload = function (event) {
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

        if (typeof userId !== "undefined" && userId !== null) {
            formData.append("user_id", userId);
        }
        
        console.log("📌 Sending image to /predict/"); 
        console.log("📌 File selected:", file.name);
        console.log("📌 File type:", file.type);

        setTimeout(() => {
            fetch("http://127.0.0.1:8000/predict", {
                method: 'POST',
                body: formData,
                headers: {
                    'Accept': 'application/json' // ✅ Siguraduhin na JSON response ang hinihingi
                }
            })
            
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                loading.style.display = 'none';

                if (data.warning) {
                    prediction.innerHTML = data.warning; // Ipakita ang warning message mula sa backend
                    
                } else {
                    prediction.innerHTML = `🌿 <strong>Herb</strong>: ${data.herb}`;
                    benefit.innerHTML = `💚 <strong>Benefits</strong>: ${data.benefit}`;
                }
            })

            .catch(async (error) => {
                loading.style.display = 'none';
                prediction.innerHTML = '❌ Prediction failed. Please check console logs.';
            
                console.error("Error fetching prediction:", error);
            
                try {
                    const errorData = await error.json();
                    console.error("Backend Error Response:", errorData);
                    prediction.innerHTML = `❌ Error: ${errorData.error || "Unknown error"}`;
                } catch (err) {
                    console.error("❌ Failed to parse error response.");
                }
            });
            
            

        }, loadingDuration);
    }

    const userId = sessionStorage.getItem("user_id") || localStorage.getItem("user_id");

    if (!userId) {
        console.warn("⚠️ No user is logged in. Proceeding as guest.");
    }
    

    // Attach event listener once HTML is fully loaded
    const fileInput = document.getElementById('imageUpload');
    if (fileInput) {
        fileInput.addEventListener('change', handleImageUpload);
        console.log("✅ Event listener added to #imageUpload");
    } else {
        if (!fileInput) {
            console.warn("⚠️ Warning: #imageUpload not found. Skipping event listener.");
            return;
        }
        
    }
});

// ✅ FIXED LOGIN FUNCTION
function login(event) {
    event.preventDefault();

    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;

    fetch("http://127.0.0.1:8000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);

        if (data.status === "success") {
            if (data.role === "admin") {
                window.location.href = "/admin_dashboard"; // Redirect sa admin dashboard
            } else {
                window.location.href = "/user_dashboard"; // Redirect sa user dashboard
            }
        }
    })
    .catch(error => {
        console.error("Login Error:", error);
    });

    closeOffcanvas(); // Close menu after login
}

// ✅ FIXED SIGNUP FUNCTION
function signup(event) {
    event.preventDefault();

    const username = document.getElementById("signupUsername").value;
    const email = document.getElementById("signupEmail").value;
    const password = document.getElementById("signupPassword").value;

    if (!username || !email || !password) {
        alert("Please fill in all fields.");
        return;
    }

    fetch("http://127.0.0.1:8000/auth/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert("Signup failed: " + data.error);
        } else {
            alert("Signup successful! Redirecting to login...");
            window.location.href = "/"; // ✅ Redirect to login page
        }
    })  
    .catch(error => {
        console.error("Signup Error:", error);
        alert("Something went wrong. Please try again.");
    });

    closeOffcanvas(); // Close menu after signup
}



// ✅ FUNCTION TO SHOW CONTENT
function showContent(sectionId) {
    document.querySelectorAll('.content, .main-wrapper, .form-container').forEach(section => {
        section.classList.add('d-none');
    });

    let section = document.getElementById(sectionId);
    if (section) {
        section.classList.remove('d-none');
    }

    document.body.style.overflow = (sectionId === 'login-form' || sectionId === 'signup-form') ? 'hidden' : 'auto';
}

// ✅ FUNCTION TO CLOSE OFFCANVAS MENU
function closeOffcanvas() {
    var offcanvas = document.getElementById('offcanvasNavbar');
    var bsOffcanvas = bootstrap.Offcanvas.getInstance(offcanvas);
    if (bsOffcanvas) {
        bsOffcanvas.hide();
    }
}