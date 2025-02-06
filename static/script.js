function submitPassword() {
    let password = document.getElementById("password").value;

    fetch('/save_password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password: password })
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => console.error('Error:', error));
}

function shareText() {
    let password = document.getElementById("password").value;
    
    if (navigator.share) {  // ✅ Check if Web Share API is supported
        navigator.share({
            title: "Shared Password",
            text: `Your password: ${password}`
        })
        .then(() => console.log("Successfully shared!"))
        .catch(error => console.error("Error sharing:", error));
    } else {
        alert("Sharing not supported in this browser.");
    }
}
