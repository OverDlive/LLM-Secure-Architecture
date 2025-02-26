import os
import subprocess
import shutil

def add_korean_font(plantuml_code: str) -> str:
    """
    PlantUML 코드 내에 'skinparam defaultFontName'이 없으면 @startuml 다음에 
    한글 지원 폰트(Malgun Gothic)를 추가합니다.
    """
    if "skinparam defaultFontName" in plantuml_code:
        return plantuml_code

    lines = plantuml_code.splitlines()
    new_lines = []
    inserted = False
    for line in lines:
        new_lines.append(line)
        if not inserted and line.strip().startswith("@startuml"):
            # @startuml 다음에 한글 폰트 설정을 추가
            new_lines.append('skinparam defaultFontName "Malgun Gothic"')
            inserted = True
    return "\n".join(new_lines)

def generate_plantuml_image(plantuml_code: str, output_file="diagram.png") -> str:
    """
    PlantUML 코드를 임시 파일(image/temp.puml)에 저장한 후, Docker 컨테이너(plantuml/plantuml)를 사용해 이미지 파일을 생성한다.
    생성된 이미지는 image 디렉토리 내에 생성된다.
    
    **추가 사항:** 컨테이너에 한글 폰트를 제공하기 위해, 현재 작업 디렉토리의 fonts 폴더를 컨테이너의
    /usr/share/fonts/truetype 경로로 마운트합니다.
    """
    # 한글 폰트 추가 (자동 삽입)
    plantuml_code = add_korean_font(plantuml_code)
    
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
    
    # fonts 디렉토리 존재 여부 확인 (호스트의 한글 폰트 파일을 저장할 곳)
    fonts_dir = os.path.join(cwd, "fonts")
    if not os.path.exists(fonts_dir):
        raise Exception("fonts 디렉토리를 찾을 수 없습니다. 한글 폰트 파일(Malgun Gothic TTF 등)을 해당 디렉토리에 추가하세요.")
    
    # image 디렉토리에 temp.puml 파일 생성
    temp_puml_file = os.path.join(image_dir, "temp.puml")
    with open(temp_puml_file, "w", encoding="utf-8") as f:
        f.write(plantuml_code)
    
    # 컨테이너 내부 작업 디렉토리 (프로젝트 루트)
    container_workdir = "/LLM-Secure-Architecture"
    container_libs_path = f"{container_workdir}/plantuml_libs"
    # 컨테이너 내부 폰트 경로: 호스트의 fonts 폴더를 /usr/share/fonts/truetype 로 마운트
    container_fonts_path = "/usr/share/fonts/truetype"
    
    try:
        # Docker 컨테이너 실행 시 전체 프로젝트 디렉토리와 폰트 디렉토리를 마운트
        command = [
            "docker", "run", "--rm",
            "-v", f"{cwd}:{container_workdir}",
            "-v", f"{fonts_dir}:{container_fonts_path}",
            "-w", container_workdir,
            "plantuml/plantuml",
            f"-Dplantuml.include.path={container_libs_path}",
            "-Dfile.encoding=UTF-8",  # 인코딩 강제 설정
            "-tpng",
            "image/temp.puml"
        ]
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except subprocess.CalledProcessError as e:
        raise Exception(f"PlantUML 이미지 생성 실패: {e.stderr.strip()}") from e
    
    # 생성된 이미지 파일 경로 (image/temp.png)
    generated_image = os.path.join(image_dir, "temp.png")
    if os.path.exists(generated_image):
        final_image_path = os.path.join(image_dir, output_file)
        if os.path.exists(final_image_path):
            os.remove(final_image_path)
        os.rename(generated_image, final_image_path)
        os.remove(temp_puml_file)
        return final_image_path
    else:
        raise Exception("PlantUML 이미지 파일이 생성되지 않았습니다.")
