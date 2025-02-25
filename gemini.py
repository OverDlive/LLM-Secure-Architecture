import os
import requests

def call_gemini_api(user_input: str) -> str:
    """
    Gemini API를 호출하여 사용자 입력에 따른 PlantUML 코드를 생성한다.
    
    실제 Gemini API 엔드포인트와 요청 파라미터, 응답 형식에 따라 아래 내용을 수정해야 합니다.
    """
    # 환경 변수에서 Gemini API 키를 가져옴
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        raise Exception("Gemini API 키가 설정되어 있지 않습니다. 환경 변수 GEMINI_API_KEY를 확인하세요.")

    # 실제 Gemini API 엔드포인트 (예시)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

    # 요청 payload: 실제 API 문서에 맞게 수정
    payload = {
        "prompt": user_input,
        "max_tokens": 512,         # 필요에 따라 조정
        "temperature": 0.7,        # 필요에 따라 조정
        # 기타 필요한 파라미터 추가
    }

    # HTTP 헤더 설정 (인증 정보 포함)
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Gemini API 호출 실패: {response.status_code} - {response.text}")

    # 응답 JSON에서 PlantUML 코드를 추출 (응답 형식에 따라 키 이름 수정)
    data = response.json()
    plantuml_code = data.get("plantuml_code")
    if not plantuml_code:
        raise Exception("Gemini API 응답에 plantuml_code 필드가 없습니다.")

    return plantuml_code
