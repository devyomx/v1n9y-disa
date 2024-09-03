// main.js

document.addEventListener("DOMContentLoaded", function () {
  const sendButton = document.getElementById("send-button");
  const userInput = document.getElementById("user-input");

  sendButton.addEventListener("click", function () {
    const message = userInput.value.trim();
    if (message) {
      // Add user message to the chat
      addMessage(message, true); // Assuming `addMessage` is defined in `animations.js`

      // Clear input field
      userInput.value = "";

      // Send message to server or perform desired action
      // ...
    }
  });

  // Handle Enter key to send message
  userInput.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      sendButton.click();
    }
  });
});
