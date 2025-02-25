// 요소 가져오기
const dropdown = document.getElementById("dropdown");
const customInput = document.getElementById("customInput");
const additionalInput = document.getElementById("additionalInput");
const generateButton = document.getElementById("generateButton");
const imageOutput = document.getElementById("imageOutput");

// 드롭다운 변경 이벤트
dropdown.addEventListener("change", () => {
  if (dropdown.value === "custom") {
    customInput.disabled = false;
    customInput.focus();
  } else {
    customInput.disabled = true;
    customInput.value = "";
  }
});

// 이미지 생성 버튼 클릭 이벤트
generateButton.addEventListener("click", async () => {
  // 사용자 입력 구성: 드롭다운 값 또는 직접 입력 + 추가 입력
  let userInput = "";
  if (dropdown.value === "custom") {
    userInput += customInput.value;
  } else {
    userInput += dropdown.value;
  }
  if (additionalInput.value) {
    userInput += "\n" + additionalInput.value;
  }

  // 버튼 상태 변경
  generateButton.disabled = true;
  generateButton.textContent = "생성 중...";

  try {
    // POST 방식으로 /generate API 호출
    const response = await fetch("/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ input: userInput })
    });
    if (!response.ok) {
      throw new Error("다이어그램 생성 중 오류 발생");
    }
    // 응답으로 받은 이미지 Blob 처리
    const blob = await response.blob();
    const imageUrl = URL.createObjectURL(blob);
    imageOutput.innerHTML = `<img src="${imageUrl}" alt="Generated Diagram">`;
  } catch (error) {
    alert("오류: " + error.message);
  } finally {
    generateButton.disabled = false;
    generateButton.textContent = "이미지 생성";
  }
});
