import os
import requests

def call_gemini_api(user_input: str) -> str:
    """
    Gemini API를 호출하여 사용자 입력에 따른 PlantUML 코드를 생성하고,
    프로젝트의 data 디렉토리에만 temp.puml 파일로 저장한다.
    """
    # 사용자 입력을 파싱하여 시스템 구성 요소와 요구사항으로 분리
    components, query = parse_user_input(user_input)
    
    # Gemini API에 전송할 프롬프트 생성
    prompt = create_prompt(components, query)

    # 환경 변수에서 Gemini API 키를 가져옴
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        raise Exception("Gemini API 키가 설정되어 있지 않습니다. 환경 변수 GEMINI_API_KEY를 확인하세요.")

    # Gemini API 엔드포인트
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={GEMINI_API_KEY}"

    # 요청 payload 구성
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "topK": 1,
            "topP": 1,
            "maxOutputTokens": 2048,
            "stopSequences": []
        },
        "safetySettings": []
    }

    # HTTP 헤더 설정
    headers = {
        "Content-Type": "application/json"
    }

    # API 요청 전송 및 응답 처리
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Gemini API 호출 실패: {response.status_code} - {response.text}")

    # 응답 JSON에서 PlantUML 코드 추출
    data = response.json()
    plantuml_code = extract_plantuml_code(data)
    if not plantuml_code:
        raise Exception("Gemini API 응답에서 PlantUML 코드를 추출할 수 없습니다.")
    
    # __file__을 기준으로 data 디렉토리 경로 생성
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # data 디렉토리 내에 temp.puml 파일만 생성
    temp_puml_path = os.path.join(data_dir, "temp.puml")
    with open(temp_puml_path, "w", encoding="utf-8") as f:
        f.write(plantuml_code)

    return plantuml_code

def parse_user_input(user_input: str) -> tuple:
    """사용자 입력을 시스템 구성 요소와 요구사항으로 분리"""
    parts = user_input.split('%')
    components = parts[0].split('^') if len(parts) > 1 else []
    query = parts[1] if len(parts) > 1 else parts[0]
    return components, query

def create_prompt(components: list, query: str) -> str:
    """Gemini API에 전송할 프롬프트 생성"""
    prompt = "시스템 구성 요소\n"
    prompt += "\n".join(components) + "\n"
    prompt += f"가 있음\n{query}\n"
    prompt += "위 요구사항을 만족하는 보안 구성도를 위한 PlantUML을 작성해줘"
    return prompt

def extract_plantuml_code(data: dict) -> str:
    """API 응답에서 PlantUML 코드 추출"""
    try:
        text = data['candidates'][0]['content']['parts'][0]['text']
        start = text.find("@startuml")
        end = text.find("@enduml")
        if start != -1 and end != -1:
            return text[start:end+7]  # @enduml 포함
        else:
            return text  # PlantUML 태그가 없는 경우 전체 텍스트 반환
    except (KeyError, IndexError):
        return None
