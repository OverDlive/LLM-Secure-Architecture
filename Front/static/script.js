const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const checkboxes = document.querySelectorAll('input[name="system"]');

function addMessage(message, isUser = false) {
  const messageElement = document.createElement('div');
  messageElement.textContent = message;
  messageElement.className = isUser ? 'user-message' : 'bot-message';
  chatMessages.appendChild(messageElement);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addImage(imageUrl) {
  const imageContainer = document.createElement('div');
  imageContainer.className = 'image-container';
  
  const imageElement = document.createElement('img');
  imageElement.src = imageUrl;
  imageElement.className = 'chat-image';
  
  imageContainer.appendChild(imageElement);
  chatMessages.appendChild(imageContainer);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function handleUserInput() {
  const message = userInput.value.trim();
  if (message) {
    const selectedSystems = Array.from(checkboxes)
      .filter(checkbox => checkbox.checked)
      .map(checkbox => checkbox.value)
      .join('^');

    const fullMessage = selectedSystems ? `${selectedSystems}%${message}` : message;
    addMessage(fullMessage, true);

    try {
      const response = await fetch('/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ input: fullMessage }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const blob = await response.blob();
      const imageUrl = URL.createObjectURL(blob);
      addImage(imageUrl);
    } catch (error) {
      console.error('Error:', error);
      addMessage(`오류 발생: ${error.message}`, false);
    }

    userInput.value = '';
  }
}

sendButton.addEventListener('click', handleUserInput);
userInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
    handleUserInput();
  }
});

