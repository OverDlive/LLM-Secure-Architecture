# 베이스 이미지 선택
FROM python:3.9-slim

# 작업 디렉터리 설정
WORKDIR /app

# 종속 파일 복사 및 설치
COPY requirements.txt .
RUN pip install -r requirements.txt

# .env 파일 복사 (보안상 주의 필요)
COPY .env .env

# 소스 코드 복사
COPY . .

# 5000 포트 노출
EXPOSE 5000

# Flask 앱 실행
CMD ["python", "app.py"]
