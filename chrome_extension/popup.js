document.addEventListener('DOMContentLoaded', function() {
    const authButton = document.getElementById('authenticate');
    const syncButton = document.getElementById('syncBlocks');
    const statusMessage = document.getElementById('statusMessage');

    authButton.addEventListener('click', function() {
        fetch(`${BACKEND_URL}/authenticate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            // Include necessary data for authentication
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                statusMessage.textContent = 'Authentication successful!';
                syncButton.style.display = 'block'; // Show the sync button
            } else {
                statusMessage.textContent = 'Authentication failed.';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            statusMessage.textContent = 'An error occurred.';
        });
    });

    syncButton.addEventListener('click', function() {
        // Similar structure for syncing logic
        // ...
    });
});
