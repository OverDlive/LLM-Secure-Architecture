import os
import subprocess

def generate_plantuml_image(plantuml_code: str, output_file="diagram.png") -> str:
    """
    PlantUML 코드를 임시 파일에 저장한 후, Docker 컨테이너(plantuml/plantuml)를 사용해 이미지 파일을 생성한다.
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
    
    # plantuml/plantuml는 temp.puml과 동일한 디렉터리에 temp.png 파일을 생성한다.
    generated_image = "temp.png"
    if os.path.exists(generated_image):
        os.rename(generated_image, output_file)
        os.remove(temp_puml_file)
        return output_file
    else:
        raise Exception("PlantUML 이미지 파일이 생성되지 않았습니다.")
