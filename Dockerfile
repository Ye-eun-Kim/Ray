FROM python:3.11-slim

EXPOSE 6023

# 작업 디렉토리 설정
WORKDIR /app

# 필수 앱 파일만 복사
COPY oliveyoung ./oliveyoung
COPY scrapy.cfg .
COPY requirements.txt .

# Python 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# PYTHONPATH 설정 - oliveyoung 모듈이 있는 디렉토리를 포함하도록
ENV PYTHONPATH "/app:${PYTHONPATH}"
ENV MONGO_URI=mongodb://mongodb-service:27017

CMD ["bash"]