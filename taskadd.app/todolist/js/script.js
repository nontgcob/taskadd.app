

function sendMessage() {
    // Get the input field and chat body
    const chatInput = document.getElementById('chatInput');
    const chatBody = document.getElementById('chatBody');

    // Get the message text
    const messageText = chatInput.value.trim();

    // Only proceed if there's a message
    if (messageText !== "") {
        // Create a new message element
        const message = document.createElement('div');
        message.className = 'message';
        message.textContent = messageText;

        // Append the message to the chat body
        chatBody.appendChild(message);

        // Scroll to the bottom
        chatBody.scrollTop = chatBody.scrollHeight;

        // Clear the input field
        chatInput.value = '';
    }
}
document.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
      sendMessage();
    }
  });    