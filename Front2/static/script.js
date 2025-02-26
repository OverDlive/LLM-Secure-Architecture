const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const checkboxes = document.querySelectorAll('input[name="system"]');

// 메시지를 채팅창에 추가하는 함수
function addMessage(message, isUser = false) {
  const messageElement = document.createElement('div');
  messageElement.textContent = message;
  messageElement.className = isUser ? 'user-message' : 'bot-message';
  chatMessages.appendChild(messageElement);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

// 이미지를 채팅창에 추가하는 함수
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

// 사용자의 입력을 처리하는 함수
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

// 체크박스를 클릭했을 때 토글 항목을 표시하거나 숨기는 함수
function toggleOptionsDisplay(checkbox) {
  const value = checkbox.value;
  const toggleOptions = document.querySelector(`.${value}-options`);
  
  if (checkbox.checked) {
    toggleOptions.style.display = 'block';
  } else {
    toggleOptions.style.display = 'none';
  }
}

// 모든 체크박스에 대해 이벤트 리스너를 추가
checkboxes.forEach(checkbox => {
  checkbox.addEventListener('change', () => toggleOptionsDisplay(checkbox));
});

// 페이지 로드 시 기본적으로 체크박스 상태를 반영
checkboxes.forEach(checkbox => {
  toggleOptionsDisplay(checkbox);
});

// 전송 버튼 클릭 시 사용자 입력 처리
sendButton.addEventListener('click', handleUserInput);

// 엔터 키 입력 시 사용자 입력 처리
userInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
    handleUserInput();
  }
});

document.addEventListener("DOMContentLoaded", function () {
  const checkboxes = document.querySelectorAll(".toggle");

  checkboxes.forEach((checkbox) => {
    checkbox.addEventListener("change", function () {
      const targetId = this.getAttribute("data-target");
      const targetDiv = document.getElementById(targetId);

      if (targetDiv) {
        targetDiv.style.display = this.checked ? "block" : "none";
      }
    });
  });
});
