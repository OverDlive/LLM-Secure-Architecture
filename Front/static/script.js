const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');



// 메시지를 채팅창에 추가하는 함수 (아이콘 포함)
function addMessage(message, isUser = false) {
    const messageElement = document.createElement('div');
    messageElement.className = isUser ? 'user-message' : 'bot-message';
    
    // 아이콘 요소 생성
    const iconElement = document.createElement('img');
    iconElement.className = 'message-icon';
    if (isUser) {
        iconElement.src = '../static/images/person.jpg';
        iconElement.alt = 'Person Icon';
    } else {
        iconElement.src = '../static/images/robot.jpg';
        iconElement.alt = 'Robot Icon';
    }
    
    
    // 텍스트 요소 생성
    const textElement = document.createElement('span');
    textElement.textContent = message;
    
    // 메시지 정렬에 따라 아이콘과 텍스트 순서 결정
    if (isUser) {
        // 사용자 메시지: 텍스트 후에 아이콘 (오른쪽 아이콘)
        messageElement.appendChild(textElement);
        messageElement.appendChild(iconElement);
    } else {
    // 봇 메시지: 아이콘 후에 텍스트 (왼쪽 아이콘)
        messageElement.appendChild(iconElement);
        messageElement.appendChild(textElement);
    }
    
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
        
        // 체크된 하위 옵션(toggle-item)만 선택, 상위 체크박스가 선택되지 않으면 들어가지 않음
        const selectedOptions = Array.from(document.querySelectorAll('.toggle-item:checked'))
            .filter(item => {
                // 상위 toggle 체크박스 찾기
                const parentToggle = item.closest('.toggle-options').previousElementSibling.querySelector('.toggle');
                // 상위 toggle이 체크된 경우에만 true 반환
                return parentToggle && parentToggle.checked;
            })
            .map(item => item.parentElement.textContent.trim())
            .filter(option => option);
        
        // 선택된 하위 옵션들을 결합
        const selectedMessage = selectedOptions.join('^');
        
        // 메시지와 선택된 하위 옵션을 결합
        const fullMessage = selectedMessage ? `${selectedMessage}%${message}` : message;
        
        // 사용자 메시지 화면에 추가 (오른쪽 정렬 + 사람 아이콘)
        addMessage(message, true);
        
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

// 모든 체크박스에 대해 이벤트 리스너 추가
document.querySelectorAll('.toggle').forEach(checkbox => {
    checkbox.addEventListener('change', function() {
        toggleOptionsDisplay(this);
    });
});

// 페이지 로드 시 기본 체크박스 상태 반영
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.toggle').forEach(checkbox => {
        toggleOptionsDisplay(checkbox);
    });
});

// 페이지 로드 시 기본 체크박스 상태 반영
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

// 브라우저 창 크기 변화에 따른 추가 UI 조정 (예: 입력창 폰트 크기 동적 조절)
window.addEventListener('resize', () => {
    const newFontSize = Math.max(14, window.innerWidth / 50);
    userInput.style.fontSize = `${newFontSize}px`;
});