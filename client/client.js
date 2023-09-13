const socket = io.connect('http://localhost:5000'); // Replace with your backend server address

socket.on('connect', () => {
    console.log('Connected to the server');
});

// Example of sending a login request to the server
const loginButton = document.getElementById('loginButton');
loginButton.addEventListener('click', () => {
    const login = document.getElementById('usernameInput').value;
    const password = document.getElementById('passwordInput').value;

    socket.emit('login', { login, password });
});

socket.on('login_response', (data) => {
    if (data.success) {
        console.log('Login successful');
        // Handle successful login, e.g., navigate to another page
    } else {
        console.log('Login failed');
        // Handle failed login, e.g., show an error message
    }
});

