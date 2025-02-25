'''
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# JSON 데이터 처리 API
@app.route("/json", methods=["POST"])
def receive_json():
    data = request.json
    return jsonify({"received_data": data})

# 이미지 업로드 API
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    return jsonify({"message": "File uploaded successfully", "file_path": file_path})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

    
----------------------------------------------------------------------
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os

app = Flask(__name__)

genai.configure(api_key='key')
model = genai.GenerativeModel('gemini-pro')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    security_requirements = request.get_json()['security']
    prompt = f"""
    다음 보안 사항을 기반으로 PlantUML 코드를 생성해주세요:
    {security_requirements}

    PlantUML 코드:
    """
    response = model.generate_content(prompt)
    return jsonify({'plantuml': response.text})

if __name__ == '__main__':
    app.run(debug=True)
'''
'''
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os
import time
import re

app = Flask(__name__)

genai.configure(api_key='AIzaSyB32BhwJqew5hr-PFqKxOcw-g6mvBgFxmY') # 여기에 실제 API 키를 입력하세요.
model = genai.GenerativeModel('gemini-pro')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    security_requirements = request.get_json()['security']
    prompt = f"""
    다음 보안 사항을 기반으로 PlantUML 코드를 생성해주세요:
    {security_requirements}

    PlantUML 코드:
    """
    response = model.generate_content(prompt)
    plantuml_code = response.text 
    # PlantUML 코드 추출

    # PlantUML 코드 저장
    timestamp = int(time.time())
    filename = f"plantuml_{timestamp}.txt"
    filepath = os.path.join("plantuml_files", filename) # plantuml_files 폴더에 저장

    # plantuml_files 폴더가 없다면 생성
    if not os.path.exists("plantuml_files"):
        os.makedirs("plantuml_files")

    with open(filepath, "w") as f:
        f.write(plantuml_code)

    return jsonify({'plantuml': plantuml_code, 'filepath': filepath}) # 파일 경로도 함께 반환
    #return jsonify({'plantuml': response.text})

if __name__ == '__main__':
    app.run(debug=True)
'''

from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os
import time
import re  # 정규식 모듈 추가

app = Flask(__name__)

genai.configure(api_key='AIzaSyB32BhwJqew5hr-PFqKxOcw-g6mvBgFxmY')  # 여기에 실제 API 키를 입력하세요.
model = genai.GenerativeModel('gemini-pro')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    security_requirements = request.get_json().get('security', '')
    prompt = f"""
    다음 보안 사항을 기반으로 PlantUML 코드를 생성해주세요:
    {security_requirements}

    PlantUML 코드:
    """
    response = model.generate_content(prompt)
    full_response = response.text  # 응답 전체 가져오기

    # 정규식으로 @startuml ~ @enduml 부분만 추출
    match = re.search(r'(@startuml.*?@enduml)', full_response, re.DOTALL)
    
    if match:
        plantuml_code = match.group(1)  # 추출된 PlantUML 코드
    else:
        plantuml_code = "No valid PlantUML code found."  # 코드가 없을 경우 예외 처리

    # 파일 저장 (txt 형식)
    timestamp = int(time.time())
    filename = f"plantuml_{timestamp}.txt"
    filepath = os.path.join("plantuml_files", filename)

    if not os.path.exists("plantuml_files"):
        os.makedirs("plantuml_files")

    with open(filepath, "w") as f:
        f.write(plantuml_code)  # 추출된 코드만 저장

    return jsonify({'plantuml': plantuml_code, 'filepath': filepath})  # JSON 응답

if __name__ == '__main__':
    app.run(debug=True)
