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

// 🔹 FETCH UPLOAD HISTORY
function fetchUploadHistory() {
    fetch("/uploads/history")
        .then(response => response.json())
        .then(data => {
            const historyBody = document.getElementById("uploadHistory");
            historyBody.innerHTML = "";

            if (data.length === 0) {
                historyBody.innerHTML = '<tr><td colspan="3">No uploads yet.</td></tr>';
            } else {
                data.forEach(upload => {
                    const row = `
                        <tr>
                            <td><img src="/uploads/${upload.image_path}" width="50"></td>
                            <td>${upload.herb_name}</td>
                            <td>${upload.upload_date}</td>
                        </tr>`;
                    historyBody.innerHTML += row;
                });
            }
        })
        .catch(error => console.error("Error fetching upload history:", error));
}

// 🔹 LOGOUT FUNCTION
function logout() {
    fetch("/auth/logout", { method: "POST" })
        .then(response => {
            if (response.ok) {
                window.location.href = "/";
            } else {
                alert("Logout failed.");
            }
        })
        .catch(error => console.error("Logout error:", error));
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

    // Check network status
    if (!navigator.onLine) {
        alert('You are offline. Please check your internet connection.');
        return;
    }

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

    setTimeout(() => {
        fetch("/predict/predict", {
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


// Logout Function
function logout() {
    fetch("/auth/logout", { method: "POST" })  // Magpadala ng POST request sa /auth/logout
        .then(response => {
            if (response.ok) {
                window.location.href = "/";  // I-redirect pabalik sa index.html
            } else {
                alert("Logout failed. Pakisubukang muli.");
            }
        })
        .catch(error => console.error("Logout error:", error));  // Magpakita ng error sa console kung may problema
}
