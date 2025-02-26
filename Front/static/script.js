const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');

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
        // 입력값을 바로 초기화하여 텍스트가 사라지도록 함
        userInput.value = '';

        // 체크된 하위 옵션(toggle-item)만 선택
        const selectedOptions = Array.from(document.querySelectorAll('.toggle-item:checked'))
            .map(item => item.parentElement.textContent.trim())
            .filter(option => option);

        // 선택된 하위 옵션들을 결합
        const selectedMessage = selectedOptions.join('^');

        // 메시지와 선택된 하위 옵션을 결합
        const fullMessage = selectedMessage ? `${selectedMessage}%${message}` : message;
        
        // 사용자 메시지 화면에 추가 (오른쪽 정렬)
        addMessage(fullMessage, true);

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

            // 서버 응답 확인 (이미지 blob을 받아와 화면에 표시)
            const blob = await response.blob();
            const imageUrl = URL.createObjectURL(blob);
            addImage(imageUrl);
        } catch (error) {
            console.error('Error:', error);
            addMessage(`오류 발생: ${error.message}`, false);
        }
    }
}

// 체크박스를 클릭했을 때 토글 항목을 표시하거나 숨기는 함수
function toggleOptionsDisplay(checkbox) {
    const targetId = checkbox.getAttribute('data-target');
    const toggleOptions = document.getElementById(targetId);
    
    if (toggleOptions) {
        toggleOptions.style.display = checkbox.checked ? 'block' : 'none';
    }
}

// 모든 체크박스에 대해 이벤트 리스너를 추가
document.querySelectorAll('.toggle').forEach(checkbox => {
    checkbox.addEventListener('change', function() {
        toggleOptionsDisplay(this);
    });
});

// 페이지 로드 시 기본적으로 체크박스 상태를 반영
document.querySelectorAll('.toggle').forEach(checkbox => {
    toggleOptionsDisplay(checkbox);
});

// 전송 버튼 클릭 시 사용자 입력 처리
sendButton.addEventListener('click', handleUserInput);

// 엔터 키 입력 시 사용자 입력 처리 및 입력창 텍스트 초기화
userInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        e.preventDefault();
        handleUserInput();
    }
});

// 브라우저 창 크기 변화에 따라 UI 크기 업데이트 (예: 입력창 폰트 크기 동적 조절)
window.addEventListener('resize', () => {
  const newFontSize = Math.max(14, window.innerWidth / 50);
  userInput.style.fontSize = `${newFontSize}px`;
});
