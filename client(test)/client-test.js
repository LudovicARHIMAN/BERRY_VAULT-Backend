// npm install socket.io-client
const io = require('socket.io-client');


const socket = io.connect('http://localhost:8080');

socket.on('connect', () => {
    console.log('Connected to server');

    // Send a message to the server
    socket.emit('message', 'Login');
});

socket.on('response', (data) => {
    console.log(`Received response from server: ${data}`);
});

socket.on('disconnect', () => {
    console.log('Disconnected from server');
});




