// static/scripts.js
document.addEventListener('DOMContentLoaded', function() {
    const balanceElement = document.getElementById('remaining-balance');

    // Fetch initial balance
    fetch('/remaining_balance/1')  // replace '1' with dynamic user ID
        .then(response => response.json())
        .then(data => {
            balanceElement.textContent = data.remaining_balance;
        });

    // SocketIO for real-time updates
    var socket = io.connect('http://localhost:5000');
    socket.on('balance_update', function(data) {
        balanceElement.textContent = data.remaining_balance;
    });
});
