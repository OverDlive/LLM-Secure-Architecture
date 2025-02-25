// 요소 가져오기
const dropdown = document.getElementById("dropdown");
const customInput = document.getElementById("customInput");
const generateButton = document.getElementById("generateButton");
const imageOutput = document.getElementById("imageOutput");

// 드롭박스 변경 이벤트
dropdown.addEventListener("change", () => {
  if (dropdown.value === "custom") {
    customInput.disabled = false; // 직접 입력 활성화
    customInput.focus();
  } else {
    customInput.disabled = true; // 직접 입력 비활성화
    customInput.value = ""; // 입력값 초기화
  }
});

// 이미지 생성 버튼 클릭 이벤트
generateButton.addEventListener("click", () => {
  alert("이미지가 생성되었습니다!"); // 팝업 메시지 표시

  // 이미지 출력 영역에 임의의 이미지 추가
  imageOutput.innerHTML = '<img src="https://via.placeholder.com/400x200" alt="생성된 이미지">';
});
