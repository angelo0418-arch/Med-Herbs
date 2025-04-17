document.addEventListener("DOMContentLoaded", function () {
    // Get the userId from sessionStorage or localStorage
    const rawUserId = sessionStorage.getItem("user_id") || localStorage.getItem("user_id");
    const userId = rawUserId && !isNaN(parseInt(rawUserId)) ? parseInt(rawUserId) : null;

    // Function to handle image upload
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

        const reader = new FileReader();
        reader.onload = function (event) {
            imagePreview.src = event.target.result;
            imagePreview.style.display = 'block';
        };
        reader.readAsDataURL(file);

        loading.style.display = 'block';
        prediction.innerHTML = '';
        benefit.innerHTML = '';

        const connection = navigator.connection || {};
        const effectiveType = connection.effectiveType || '4g';
        const loadingDuration = (effectiveType === '4g' || !effectiveType) ? 1000 : 3000;

        const formData = new FormData();
        formData.append('file', file);

        // If user is logged in and user_id is a valid number, append it
        if (userId !== null) {
            formData.append("user_id", userId);
            console.log("📌 Logged-in user ID:", userId);
        } else {
            // If not logged in, generate or get guest_id from localStorage
            let guestId = localStorage.getItem("guest_id");
            if (!guestId) {
                guestId = 'guest_' + Date.now();
                localStorage.setItem("guest_id", guestId);
            }
            formData.append("guest_id", guestId);
            console.log("📌 Guest ID:", guestId);
        }

        console.log("📌 Sending image to /predict/"); 
        console.log("📌 File selected:", file.name);
        console.log("📌 File type:", file.type);

        setTimeout(() => {
            fetch("http://127.0.0.1:8000/predict", {
                method: 'POST',
                body: formData,
                headers: {
                    'Accept': 'application/json'
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
                    prediction.innerHTML = data.warning;
                } else {
                    prediction.innerHTML = `
                    <div class="herb-details">
                        <div class="herb-item">
                            <div class="herb-label">🌿 Scientific Name:</div>
                            <div class="herb-value">${data.scientific_name}</div>
                        </div>
                        <div class="herb-item">
                            <div class="herb-label">🌿 English Name:</div>
                            <div class="herb-value">${data.english_name}</div>
                        </div>
                        <div class="herb-item">
                            <div class="herb-label">🌿 Tagalog Name:</div>
                            <div class="herb-value">${data.tagalog_name}</div>
                        </div>
                        <div class="herb-item">
                            <div class="herb-label">🌿 Bicol Name:</div>
                            <div class="herb-value">${data.bicol_name}</div>
                        </div>
                    </div>
                
                    <div class="herb-description">
                        📖 <strong>Description:</strong> ${data.description}
                    </div>
                `;
                
                benefit.innerHTML = `
                    <div class="herb-benefit">
                        💚 <strong>Benefits:</strong> ${data.benefit}
                    </div>
                `;
                
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

    // Add event listener for image upload
    const fileInput = document.getElementById('imageUpload');
    if (fileInput) {
        fileInput.addEventListener('change', handleImageUpload);
        console.log("✅ Event listener added to #imageUpload");
    } else {
        console.warn("⚠️ Warning: #imageUpload not found. Skipping event listener.");
        return;
    }
});

// ✅ LOGIN FUNCTION
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
            sessionStorage.setItem("user_id", data.user_id);

            if (data.role === "admin") {
                window.location.href = "/admin_dashboard";
            } else {
                window.location.href = "/user_dashboard";
            }
        }
    })
    .catch(error => {
        console.error("Login Error:", error);
    });

    closeOffcanvas();
}

// ✅ SIGNUP FUNCTION
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
            window.location.href = "/";
        }
    })  
    .catch(error => {
        console.error("Signup Error:", error);
        alert("Something went wrong. Please try again.");
    });

    closeOffcanvas();
}

// ✅ SHOW CONTENT FUNCTION
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

// ✅ CLOSE OFFCANVAS MENU
function closeOffcanvas() {
    var offcanvasElement = document.querySelector('.offcanvas.show');
    if (offcanvasElement) {
        var offcanvas = bootstrap.Offcanvas.getInstance(offcanvasElement);
        if (offcanvas) {
            offcanvas.hide();
        }
    }
}