# 베이스 이미지 변경
FROM python:3.8.18-slim

# Expose Telnet console port
EXPOSE 6023

# 작업 디렉토리 설정
WORKDIR /usr/src/app

# 애플리케이션 코드 복사
COPY ./oliveyoung ./oliveyoung

# scrapy.cfg 파일 복사
COPY scrapy.cfg .

# 요구 사항 파일 복사
COPY requirements.txt ./

# Python 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# PYTHONPATH 설정
ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV MONGO_URI=mongodb://mongodb-service:27017


# 기본 실행 커맨드 설정
CMD ["bash"]
