document.addEventListener("DOMContentLoaded", function () {
    fetchUserData();
    attachImageUploadListener();
});

// 🔹 FETCH USER DATA
function fetchUserData() {
    fetch("/auth/check_session")
        .then(response => response.json())
        .then(data => {
            if (data.logged_in) {
                document.getElementById("username").innerText = data.username;
                fetchUploadHistory();
            } else {
                window.location.href = "/";
            }
        })
        .catch(error => console.error("Error fetching user data:", error));
}


// 🔹 TOGGLE PROFILE VIEW
function toggleProfile() {
    const profileSection = document.getElementById('profileSection');
    profileSection.style.display = profileSection.style.display === 'none' ? 'block' : 'none';
}

// 🔹 SHOW SPECIFIC CONTENT
function showContent(sectionId) {
    const sections = ['main-wrapper', 'user-guide', 'about'];

    sections.forEach(id => {
        const section = document.getElementById(id);
        if (section) {
            section.classList.toggle('d-none', id !== sectionId);
        }
    });

    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.scrollIntoView({ behavior: 'smooth' });
    }

    // I-close ang offcanvas pagkatapos mag-click ng link
    closeOffcanvas();
}

// 🔹 HANDLE IMAGE UPLOAD
function attachImageUploadListener() {
    const fileInput = document.getElementById('imageUpload');
    if (fileInput) {
        fileInput.addEventListener('change', handleImageUpload);
        console.log("✅ Event listener added to #imageUpload");
    } else {
        console.error("❌ Element #imageUpload not found in DOM!");
    }
}

function handleImageUpload() {
    const fileInput = document.getElementById('imageUpload');
    const file = fileInput?.files[0]; 
    const loading = document.getElementById('loading');
    const prediction = document.getElementById('prediction');
    const benefit = document.getElementById('benefit');
    const imagePreview = document.getElementById('imagePreview');

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

    // Show loading animation
    loading.style.display = 'block';
    prediction.innerHTML = '';
    benefit.innerHTML = '';

    // Adjust loading speed based on network signal
    const connection = navigator.connection || {};
    const effectiveType = connection.effectiveType || '4g';
    const loadingDuration = (effectiveType === '4g' || !effectiveType) ? 1000 : 3000;

    // Prepare FormData for upload
    const formData = new FormData();
    formData.append('file', file);

    // ✅ GET USER ID FROM SESSION
    const rawUserId = sessionStorage.getItem("user_id");
    const userId = rawUserId && !isNaN(parseInt(rawUserId)) ? parseInt(rawUserId) : null;

    if (userId !== null) {
        formData.append("user_id", userId);
        console.log("📌 Logged-in user ID:", userId);
    } else {
        console.warn("⚠️ No user_id found in sessionStorage.");
    }

    setTimeout(() => {
        fetch("/predict", {
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
                prediction.innerHTML = '❌ ' + (data.error || 'Prediction failed. Please try again.');
            } else if (data.warning) {
                prediction.innerHTML = '⚠️ ' + data.warning;
            }else {
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
        .catch(error => {
            loading.style.display = 'none';
            prediction.innerHTML = '❌ Prediction failed. Please try again.';
            console.error("Error fetching prediction:", error);
        });
    }, loadingDuration);
}

function logout(event) {
    if (event) {
        event.stopPropagation(); // Para sa dropdown logout
    }

    // 🔹 Desktop logout elements
    const logoutBtn = document.getElementById("logoutBtn");
    const logoutSpinner = document.getElementById("logoutSpinner");

    // 🔹 Mobile logout elements
    const logoutBtnMobile = document.getElementById("logoutBtnMobile");
    const logoutSpinnerMobile = document.getElementById("logoutSpinnerMobile");

    // Disable desktop button and show spinner
    if (logoutBtn && logoutSpinner) {
        logoutBtn.style.pointerEvents = "none";
        logoutSpinner.style.display = "inline-block";
    }

    // 🔥 Disable mobile button and show spinner
    if (logoutBtnMobile && logoutSpinnerMobile) {
        logoutBtnMobile.style.pointerEvents = "none";
        logoutSpinnerMobile.style.display = "inline-block";
    }

    fetch("/auth/logout", { method: "POST" })
        .then(response => {
            if (response.ok) {
                setTimeout(() => {
                    window.location.href = "/";
                }, 2000);
            } else {
                alert("❌ Logout failed. Pakisubukang muli.");

                // Re-enable both desktop & mobile logout buttons
                if (logoutBtn && logoutSpinner) {
                    logoutBtn.style.pointerEvents = "auto";
                    logoutSpinner.style.display = "none";
                }
                if (logoutBtnMobile && logoutSpinnerMobile) {
                    logoutBtnMobile.style.pointerEvents = "auto";
                    logoutSpinnerMobile.style.display = "none";
                }
            }
        })
        .catch(error => {
            console.error("❌ Logout error:", error);
            alert("❌ May problema sa logout. Pakisubukang muli.");

            // Re-enable both desktop & mobile logout buttons
            if (logoutBtn && logoutSpinner) {
                logoutBtn.style.pointerEvents = "auto";
                logoutSpinner.style.display = "none";
            }
            if (logoutBtnMobile && logoutSpinnerMobile) {
                logoutBtnMobile.style.pointerEvents = "auto";
                logoutSpinnerMobile.style.display = "none";
            }
        });
}


// 🔹 CLOSE OFFCANVAS
function closeOffcanvas() {
    var offcanvasElement = document.getElementById('offcanvasNavbar');
    if (offcanvasElement) {
        var offcanvas = bootstrap.Offcanvas.getInstance(offcanvasElement);
        if (offcanvas) {
            offcanvas.hide(); // isara yung offcanvas
        }
    }
}