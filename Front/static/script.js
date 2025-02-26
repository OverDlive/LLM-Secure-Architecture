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
        // 체크된 하위 옵션(toggle-item)만 선택
        const selectedOptions = Array.from(document.querySelectorAll('.toggle-item:checked'))
            .map(item => item.parentElement.textContent.trim())
            .filter(option => option); // 필터링을 통해 선택된 항목만 반환

        // 선택된 하위 옵션들을 결합
        const selectedMessage = selectedOptions.join('^');

        // 메시지와 선택된 하위 옵션을 결합
        const fullMessage = selectedMessage ? `${selectedMessage}%${message}` : message;
        
        // 사용자 메시지 화면에 추가
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

            // 서버 응답 확인
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            // 서버로부터 받은 응답 처리
            const blob = await response.blob();
            const imageUrl = URL.createObjectURL(blob);
            addImage(imageUrl); // 응답으로 받은 이미지를 화면에 표시
        } catch (error) {
            console.error('Error:', error);
            addMessage(`오류 발생: ${error.message}`, false); // 오류 메시지 표시
        }

        // 입력창 초기화
        userInput.value = ''; 
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

// 엔터 키 입력 시 사용자 입력 처리
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        handleUserInput();
    }
});