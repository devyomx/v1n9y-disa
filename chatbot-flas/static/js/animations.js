document.addEventListener("DOMContentLoaded", function () {
  const messagesContainer = document.getElementById("messages");

  function addMessage(text, isUser) {
    const message = document.createElement("div");
    message.classList.add("message", isUser ? "user-message" : "bot-message");
    message.textContent = text;
    messagesContainer.appendChild(message);

    // Trigger fade-in effect
    setTimeout(() => {
      message.style.opacity = 1;
    }, 10);

    messagesContainer.scrollTop = messagesContainer.scrollHeight; // Auto-scroll to the latest message
  }

  // Example usage (can be removed or modified as needed)
  addMessage("Hello, how can I help you?", false); // Adding a bot message
});
