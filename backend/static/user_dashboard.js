document.addEventListener("DOMContentLoaded", function () {
    fetchUserData();
});

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

function fetchUploadHistory() {
    fetch("/uploads/history")
        .then(response => response.json())
        .then(data => {
            const historyBody = document.getElementById("uploadHistoryBody");
            historyBody.innerHTML = "";  // Clear previous entries

            data.forEach(upload => {
                const row = `<tr>
                    <td><img src="/uploads/${upload.image_path}" width="50"></td>
                    <td>${upload.herb_name}</td>
                    <td>${upload.upload_date}</td>
                </tr>`;
                historyBody.innerHTML += row;
            });
        })
        .catch(error => console.error("Error fetching upload history:", error));
}

// Logout Function
document.getElementById("logoutBtn").addEventListener("click", function () {
    fetch("/auth/logout", { method: "POST" })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = "/";
            }
        })
        .catch(error => console.error("Logout error:", error));
});
