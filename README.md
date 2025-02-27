![header](https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=10&height=200&text=LLM%20Secure%20Architecture&fontSize=40&animation=twinkling&fontAlign=68&fontAlignY=36)

## 💡소개

이 프로젝트는 정보보호 아키텍처 설계를 자동화하기 위한 Llama 기반 챗봇 시스템으로, 복잡한 설계를 보다 효율적으로 수행할 수 있도록 돕습니다. 기존 UML 모델링 방식이 수작업으로 진행되어 시간이 오래 걸리고 오류가 발생할 수 있는 문제점을 해결하기 위해, 대규모 언어 모델(LLM)을 활용하여 정보보호 아키텍처의 복잡성을 완화하고 자동화 및 효율적 문서화/표준화를 지원합니다.

---

## 📖프로젝트 구조
```
|-- Dockerfile
|-- Front
|   |-- __pycache__
|   |   `-- app.cpython-312.pyc
|   |-- static
|   |   |-- script.js
|   |   `-- styles.css
|   `-- templates
|       `-- index.html
|-- LICENSE
|-- README.md
|-- __pycache__
|   |-- app.cpython-312.pyc
|   |-- gemini.cpython-312.pyc
|   |-- plantuml_generator.cpython-312.pyc
|   `-- uml_include_replacer.cpython-312.pyc
|-- app.py
|-- data
|   `-- temp.puml
|-- gemini.py
|-- image
|   |-- temp.png
|   `-- temp.puml
|-- plantuml_generator.py
|-- plantuml_libs
|   |-- C4.puml
|   |-- C4_Component.puml
|   |-- C4_Container.puml
|   |-- C4_Context.puml
|   |-- C4_Deployment.puml
|   `-- C4_Dynamic.puml
|-- requirements.txt
`-- uml_include_replacer.py

8 directories, 25 files
```
---

## ⚙️주요 기능

1. 자동화된 UML 설계 지원: Llama(LLM) 기반 챗봇을 통해 아키텍처 초안 설계.

2. 보안 시스템 모델링: Flask 백엔드와 연동하여, 사용자의 요구사항에 맞춰 보안 위협 및 대응 전략 등 정보보호 요소를 시각화.

3. 표준 문서 자동생성: UML 다이어그램 설계와 함께 보안 요구사항 문서, 아키텍처 설계서 등을 자동으로 생성.

4. 클라우드 연동: GCP 환경을 통해 확장 가능하고 안정적인 서버 운영.

5. 간단한 개발 및 배포: Python 기반 Flask, GCP 연동으로 개발 및 배포 프로세스를 단순화.

---

## 👩‍💻팀원

|<img src="https://avatars.githubusercontent.com/u/66999301?s=400&v=4" width="150" height="150"/>|<img src="https://avatars.githubusercontent.com/u/74577816?v=4" width="150" height="150"/>|<img src="https://avatars.githubusercontent.com/u/108620416?v=4" width="150" height="150"/>|<img src="https://avatars.githubusercontent.com/u/191064967?v=4" width="150" height="150"/>
|:-:|:-:|:-:|:-:|
|한동혁<br/>[@OverDlive](https://github.com/OverDlive)<br/>PM, 백엔드|박보현<br/>[@BBoMan](https://github.com/BBoMan)<br/>백엔드, 프론트엔드 ui|송윤지<br/>[@roongzee](https://github.com/roongzee)<br/>Gemini api 연동동|유가영<br/>[@yoo8543](https://github.com/yoo8543)<br/>네트워크 구성 요소 분석석|
---

## 🚨주의사항
LLM 응답은 상황에 따라 달라질 수 있으므로, 보안 아키텍처 적합성을 위해 반드시 리뷰/검증 과정이 필요합니다.

GCP 리소스 설정(프로젝트 ID, 인증키 등)을 올바르게 설정해야 정상 동작합니다.

---

## 📲실행방법
1. 리눅스 서버에 docker 설치
    ```bash
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    ```
2. flask app 실행
    ```bash
    flask run
    ```

---
<div align=center><h1>📚 STACKS</h1></div>
  <div align=center> 
      <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> 
    <br>
      <img src="https://img.shields.io/badge/html5-E34F26?style=for-the-badge&logo=html5&logoColor=white"> 
      <img src="https://img.shields.io/badge/css-1572B6?style=for-the-badge&logo=css3&logoColor=white"> 
      <img src="https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black"> 
    <br>
      <img src="https://img.shields.io/badge/flask-000000?style=for-the-badge&logo=flask&logoColor=white">
    <br>
      <img src="https://img.shields.io/badge/linux-FCC624?style=for-the-badge&logo=linux&logoColor=black">
    <br>
    <img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white">
    <img src="https://img.shields.io/badge/git-F05032?style=for-the-badge&logo=git&logoColor=white">
  <br></div>

---
## 📑라이선스

- 본 프로젝트는 MIT 라이선스를 사용합니다. 자세한 내용은 LICENSE 파일을 참고하시기 바랍니다.

---

## 📞문의

- 프로젝트 관련 문의 사항이나 개선 제안은 팀원에게 직접 혹은 이슈 트래커(깃 저장소 등)를 통해 남겨주시기 바랍니다.

---

위의 내용은 프로토타입 단계에 중점을 둔 것이며, 추가적인 기능 확장 및 보안 테스트, 운영 환경에 맞춘 최적화 작업이 필요할 수 있습니다. 지속적으로 문서를 업데이트해가며 개선할 예정입니다.

