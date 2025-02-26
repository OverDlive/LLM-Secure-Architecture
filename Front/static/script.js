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
  const userInput = document.getElementById('user-input');
  const message = userInput.value.trim();
  
  if (message) {
    // 체크된 하위 옵션만 처리 (클라이언트, 네트워크, 서버, 애플리케이션, DB)
    const selectedOptions = Array.from(document.querySelectorAll('.checkbox-container input[type="checkbox"]:checked'))
      .map(checkbox => {
        const targetId = checkbox.getAttribute('data-target');
        const options = Array.from(document.querySelectorAll(`#${targetId} .toggle-item:checked`))
          .map(item => item.parentElement.textContent.trim());
        return options;  // 하위 옵션만 반환
      })
      .flat();  // 다차원 배열을 평평하게 만듬 (배열의 배열 형태로 반환되는 걸 해결)

    // 선택된 하위 옵션들을 결합
    const selectedMessage = selectedOptions.join(', ');

    // 메시지와 선택된 하위 옵션을 결합
    const fullMessage = selectedMessage ? `${selectedMessage}^${message}` : message;
    
    addMessage(fullMessage, true);  // 사용자 메시지 추가

    try {
      // 서버로 요청 전송
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

      // 서버로부터 받은 응답 처리
      const blob = await response.blob();
      const imageUrl = URL.createObjectURL(blob);
      addImage(imageUrl);  // 응답으로 받은 이미지를 화면에 표시
    } catch (error) {
      console.error('Error:', error);
      addMessage(`오류 발생: ${error.message}`, false);  // 오류 메시지 표시
    }

    userInput.value = '';  // 입력창 초기화
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
