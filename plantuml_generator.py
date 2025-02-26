import os
import subprocess
import shutil

def generate_plantuml_image(plantuml_code: str, output_file="diagram.png") -> str:
    """
    PlantUML 코드를 임시 파일에 저장한 후, Docker 컨테이너(plantuml/plantuml)를 사용해 이미지 파일을 생성한다.
    생성된 이미지는 image 디렉토리 내에 생성된다.
    """
    # Docker 명령어가 사용 가능한지 확인
    if shutil.which("docker") is None:
        raise Exception("Docker 명령어를 찾을 수 없습니다. Docker가 설치되어 있고 PATH에 등록되어 있는지 확인하세요.")
    
    # image 디렉토리가 존재하지 않으면 생성
    image_dir = os.path.join(os.getcwd(), "image")
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    
    # image 디렉토리에 temp.puml 파일 생성
    temp_puml_file = os.path.join(image_dir, "temp.puml")
    with open(temp_puml_file, "w", encoding="utf-8") as f:
        f.write(plantuml_code)
    
    # Docker 컨테이너에서 /data 로 마운트하도록 image 디렉토리를 지정
    try:
        result = subprocess.run([
            "docker", "run", "--rm",
            "-v", f"{image_dir}:/data",   # image 디렉토리를 컨테이너의 /data로 마운트
            "plantuml/plantuml", "-tpng", "/data/temp.puml"
        ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # 필요에 따라 result.stdout/result.stderr 로깅 가능
    except subprocess.CalledProcessError as e:
        raise Exception(f"PlantUML 이미지 생성 실패: {e.stderr.strip()}") from e
    
    # Docker 컨테이너가 생성한 이미지 파일 경로 (image/temp.png)
    generated_image = os.path.join(image_dir, "temp.png")
    if os.path.exists(generated_image):
        final_image_path = os.path.join(image_dir, output_file)
        os.rename(generated_image, final_image_path)
        os.remove(temp_puml_file)
        return final_image_path
    else:
        raise Exception("PlantUML 이미지 파일이 생성되지 않았습니다.")
