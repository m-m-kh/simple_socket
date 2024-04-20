const socket = new WebSocket('ws://localhost:8765');

socket.addEventListener('open', function (event) {
    console.log('Connected to WebSocket server');
});

socket.addEventListener('message', function (event) {
    console.log('Message from server:', event.data);
    // socket.send('Hello, WebSocket Server!');
});

socket.addEventListener('close', function (event) {
    console.log('Disconnected from WebSocket server');
});


socket.addEventListener('error', function (event) {
    console.error('WebSocket error:', event);
});