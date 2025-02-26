import os
import subprocess
import shutil

def generate_plantuml_image(plantuml_code: str, output_file="diagram.png") -> str:
    """
    PlantUML 코드를 임시 파일(image/temp.puml)에 저장한 후, Docker 컨테이너(plantuml/plantuml)를 사용해 이미지 파일을 생성한다.
    생성된 이미지는 image 디렉토리 내에 생성된다.
    """
    # Docker 명령어가 사용 가능한지 확인
    if shutil.which("docker") is None:
        raise Exception("Docker 명령어를 찾을 수 없습니다. Docker가 설치되어 있고 PATH에 등록되어 있는지 확인하세요.")
    
    cwd = os.getcwd()
    
    # image 디렉토리가 존재하지 않으면 생성
    image_dir = os.path.join(cwd, "image")
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    
    # plantuml_libs 디렉토리 존재 여부 확인
    plantuml_libs_dir = os.path.join(cwd, "plantuml_libs")
    if not os.path.exists(plantuml_libs_dir):
        raise Exception("plantuml_libs 디렉토리를 찾을 수 없습니다.")
    
    # image 디렉토리에 temp.puml 파일 생성
    temp_puml_file = os.path.join(image_dir, "temp.puml")
    with open(temp_puml_file, "w", encoding="utf-8") as f:
        f.write(plantuml_code)
    
    # 컨테이너 내부 작업 디렉토리 (프로젝트 루트)
    container_workdir = "/LLM-Secure-Architecture"
    # 컨테이너 내부의 라이브러리 경로 (Linux 스타일)
    container_libs_path = f"{container_workdir}/plantuml_libs"
    
    try:
        # Docker 컨테이너 실행 (전체 프로젝트를 마운트)
        command = [
            "docker", "run", "--rm",
            "-v", f"{cwd}:{container_workdir}",
            "-w", container_workdir,  # 작업 디렉토리 설정 (프로젝트 루트)
            "plantuml/plantuml",
            f"-Dplantuml.include.path={container_libs_path}",  # 라이브러리 포함 경로 지정
            "-tpng",
            "image/temp.puml"  # image 폴더 내의 temp.puml 파일 사용
        ]
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except subprocess.CalledProcessError as e:
        raise Exception(f"PlantUML 이미지 생성 실패: {e.stderr.strip()}") from e
    
    # Docker 컨테이너가 생성한 이미지 파일 경로 (image/temp.png)
    generated_image = os.path.join(image_dir, "temp.png")
    if os.path.exists(generated_image):
        final_image_path = os.path.join(image_dir, output_file)
        # 대상 파일이 존재하면 삭제
        if os.path.exists(final_image_path):
            os.remove(final_image_path)
        os.rename(generated_image, final_image_path)
        os.remove(temp_puml_file)
        return final_image_path
    else:
        raise Exception("PlantUML 이미지 파일이 생성되지 않았습니다.")

