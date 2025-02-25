import os
import subprocess
from flask import Flask, render_template, request, send_file, jsonify
from dotenv import load_dotenv

load_dotenv()  # .env 파일에 GEMINI_API_KEY 등 환경변수를 저장

# Front 폴더 내 static 및 templates 경로 지정
static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Front', 'static')
template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Front', 'templates')

app = Flask(__name__, static_folder=static_folder, template_folder=template_folder)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True

def call_gemini_api(user_input: str) -> str:
    """
    Gemini API를 호출해 사용자 입력에 따른 PlantUML 코드를 생성한다.
    
    실제 Gemini API 문서에 따라 엔드포인트, 요청 파라미터, 헤더 등을 수정해야 합니다.
    아래 예시는 가상의 엔드포인트와 요청 형식을 사용한 예시입니다.
    """
    # 환경 변수에서 Gemini API 키를 가져옴
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        raise Exception("Gemini API 키가 설정되어 있지 않습니다. 환경 변수 GEMINI_API_KEY를 확인하세요.")

    # Gemini API의 실제 엔드포인트로 변경
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=GEMINI_API_KEY"

    # 요청 payload: 실제 Gemini API 문서에 따라 요청 데이터 구성
    payload = {
        "prompt": user_input,
        "max_tokens": 512,         # 생성할 최대 토큰 수 (필요에 따라 조정)
        "temperature": 0.7,        # 생성 온도 (필요에 따라 조정)
        # 기타 필요한 파라미터 추가
    }

    # HTTP 헤더 설정 (인증 정보 포함)
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }

    # Gemini API 호출
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Gemini API 호출 실패: {response.status_code} - {response.text}")

    # 응답 JSON에서 PlantUML 코드를 추출 (실제 응답 형식에 따라 키 이름을 수정)
    data = response.json()
    plantuml_code = data.get("plantuml_code")
    if not plantuml_code:
        raise Exception("Gemini API 응답에 plantuml_code 필드가 없습니다.")

    return plantuml_code

# ----- PlantUML 코드 → 이미지 변환 (Docker 사용) -----
def generate_plantuml_image(plantuml_code: str, output_file="diagram.png") -> str:
    """
    PlantUML 코드를 임시 파일에 저장한 후, Docker 컨테이너(plantuml/plantuml)를 실행해 이미지 파일을 생성한다.
    """
    temp_puml_file = "temp.puml"
    with open(temp_puml_file, "w", encoding="utf-8") as f:
        f.write(plantuml_code)
    
    docker_command = [
        "docker", "run", "--rm",
        "-v", f"{os.getcwd()}:/workspace",
        "plantuml/plantuml",
        temp_puml_file
    ]
    try:
        subprocess.run(docker_command, check=True)
    except subprocess.CalledProcessError as e:
        raise Exception(f"PlantUML 이미지 생성 실패: {e}")
    
    # plantuml/plantuml 기본 동작: temp.puml → temp.png
    generated_image = "temp.png"
    if os.path.exists(generated_image):
        os.rename(generated_image, output_file)
        os.remove(temp_puml_file)
        return output_file
    else:
        raise Exception("PlantUML 이미지 파일이 생성되지 않았습니다.")

# ----- 기본 페이지 렌더링 -----
@app.route('/')
def home():
    return render_template('index.html')

# ----- UML 다이어그램 생성 API -----
@app.route('/generate', methods=['POST'])
def generate_diagram():
    """
    클라이언트에서 전달된 JSON 데이터({ "input": "..." })를 받아 Gemini API로 PlantUML 코드를 생성한 후,
    Docker를 통해 UML 다이어그램 이미지를 생성해 반환한다.
    """
    data = request.get_json()
    if not data or "input" not in data:
        return jsonify({"error": "입력 데이터가 올바르지 않습니다."}), 400

    user_input = data["input"]
    try:
        # 1. Gemini API를 통해 PlantUML 코드 생성
        plantuml_code = call_gemini_api(user_input)
        print("Generated PlantUML Code:\n", plantuml_code)

        # 2. PlantUML 코드를 이미지로 변환
        image_path = generate_plantuml_image(plantuml_code)
        
        # 3. 생성된 이미지 파일을 클라이언트에 반환
        return send_file(image_path, mimetype="image/png")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # 개발 시 debug=True, 실제 배포 시 적절한 설정 사용
    app.run(debug=True)
