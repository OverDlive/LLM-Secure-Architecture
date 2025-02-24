![header](https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=10&height=200&text=Snort%20Automatic%20diagnosis&fontSize=40&animation=twinkling&fontAlign=68&fontAlignY=36)
## 소개

이 프로젝트는 Google Cloud 환경에서 Snort를 이용해 네트워크 침입 탐지 시스템(IDS)을 구성하고, 수집된 로그를 클라우드로 전송 및 처리한 뒤, 웹 기반 GUI로 모니터링하는 것이 목표입니다. 추가로, LLM(Llama API) 연동을 통해 Snort 결과 데이터를 자연어로 해석하고, 사용자 친화적인 정보를 제공하는 기능을 포함하고 있습니다.

---

## 프로젝트 구조

1. **Google Cloud 기반 Snort 백엔드**
   - Google Cloud Compute Engine 또는 Kubernetes Engine에서 Snort를 구동
   - `snort.conf` 및 `local.rules` 파일을 활용하여 규칙 기반 침입 탐지 구현
   - Barnyard2 또는 자체 스크립트를 사용해 로그를 Pub/Sub, Cloud Storage, Cloud SQL 등 클라우드 서비스로 전송

2. **로그 수집 및 후처리**
   - Cloud Functions 등으로 실시간 혹은 주기적으로 로그를 파싱
   - API 서버를 통해 클라이언트(웹)에서 필요한 데이터를 요청할 수 있도록 구성

3. **웹 기반 GUI 인터페이스**
   - React, Vue 등 프론트엔드 프레임워크 또는 기본 HTML/CSS/JavaScript로 개발
   - 실시간 알림 및 로그 데이터를 표시하는 대시보드
   - 패킷/알림 목록과 상세 정보를 열람할 수 있는 기능

4. **LLM 해석 모듈**
   - LLM API(예: Llama API)에 로그 데이터를 전달해 자연어로 된 해석을 획득
   - 웹 GUI에서 상세 설명 및 요약 정보 확인 가능

---

## 주요 기능

- **IDS(침입 탐지)**: Snort 규칙 기반으로 네트워크 침입을 식별 및 경고 생성
- **로그 수집 및 관리**: 생성된 로그를 중앙화된 GCP 환경에서 저장 및 관리
- **실시간 대시보드**: 웹 UI를 통해 스니핑된 패킷과 알림 정보를 실시간으로 모니터링
- **LLM 분석**: Snort 결과를 LLM으로 전달해 사용자 친화적인 설명과 분석 제공

---

## 설치 및 실행 가이드 (프로토타입 기준)

1. **Google Cloud 환경 설정**
   - 프로젝트 생성 및 Compute Engine/Kubernetes Engine 활성화
   - 방화벽, VPC 설정 등 네트워크 관련 구성

2. **Snort 설치 및 설정**
   - Google Cloud 인스턴스나 컨테이너에 Snort 설치
   - `snort.conf`와 `local.rules`로 초기 규칙 작성
   - 테스트를 통해 룰 및 네트워크 트래픽 검증

3. **로그 전송 및 처리**
   - Barnyard2 등을 활용해 로그를 Pub/Sub 혹은 Cloud Storage로 전송
   - Cloud Functions 또는 별도의 워커에서 로그를 파싱하고 DB나 스토리지에 저장

4. **웹 UI 구성**
   - React/Vue 또는 HTML/CSS/JS로 웹 대시보드 개발
   - API 서버와 연동해 실시간 데이터 제공

5. **LLM 모듈 연동**
   - Llama API 등의 LLM 연결
   - 사용자 입력이나 경고 클릭 시 로그 분석 결과를 LLM에 전달
   - 반환된 자연어 응답을 UI에서 표시

---

## 프로젝트 일정 (3일 프로토타입)

- **Day 1**: Google Cloud 및 Snort 백엔드 구성
  - GCP 인스턴스/Kubernetes 설정, Snort 설치
  - 룰 파일 설정 및 로그 전송 방법 세팅

- **Day 2**: 로그 처리 및 GUI 구축
  - 로그 저장 및 후처리 로직(Cloud Functions or 기타 방식)
  - 웹 대시보드(리스트, 상세 정보, 실시간 모니터링) 구현

- **Day 3**: LLM 연동 및 통합 테스트
  - LLM API 연동 모듈 추가
  - 전체 시스템 통합 및 성능 테스트

---

## 팀원

|<img src="https://avatars.githubusercontent.com/u/66999301?s=400&v=4" width="150" height="150"/>|<img src="https://avatars.githubusercontent.com/u/74577816?v=4" width="150" height="150"/>|<img src="https://avatars.githubusercontent.com/u/108620416?v=4" width="150" height="150"/>|<img src="https://avatars.githubusercontent.com/u/191064967?v=4" width="150" height="150"/>
|:-:|:-:|:-:|:-:|
|한동혁<br/>[@OverDlive](https://github.com/OverDlive)<br/>PM, 백엔드|박보현<br/>[@BBoMan](https://github.com/BBoMan)<br/>백엔드, 프론트엔드 ui|송윤지<br/>[@roongzee](https://github.com/roongzee)<br/>snort 진단|유가영<br/>[@yoo8543](https://github.com/yoo8543)<br/>Llama api 관리|
---

## 라이선스

- 본 프로젝트는 MIT 라이선스를 사용합니다. 자세한 내용은 LICENSE 파일을 참고하시기 바랍니다.

---

## 문의

- 프로젝트 관련 문의 사항이나 개선 제안은 팀원에게 직접 혹은 이슈 트래커(깃 저장소 등)를 통해 남겨주시기 바랍니다.

---

위의 내용은 프로토타입 단계에 중점을 둔 것이며, 추가적인 기능 확장 및 보안 테스트, 운영 환경에 맞춘 최적화 작업이 필요할 수 있습니다. 지속적으로 문서를 업데이트해가며 개선할 예정입니다.

