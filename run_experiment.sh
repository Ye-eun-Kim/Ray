#!/bin/bash

# 로그 파일 이름 설정
BASE_LOG_FILE="experiment_log.txt"

# 로그 파일 이름 중복 처리
LOG_FILE="$BASE_LOG_FILE"
COUNTER=1
while [[ -f "$LOG_FILE" ]]; do
    LOG_FILE="${BASE_LOG_FILE%.txt}_$COUNTER.txt"
    COUNTER=$((COUNTER + 1))
done

# MongoDB 설정
DB_NAME="olive_db"
COLLECTION_NAME="products"

# 현재 날짜 및 시간 기록
echo "실험 시작: $(date)" >> "$LOG_FILE"
echo "======================" >> "$LOG_FILE"

# 3. python ./oliveyoung/spiders/product_no_ray.py 실행
echo "3. product_no_ray.py 실행 중..." >> "$LOG_FILE"
NO_RAY_OUTPUT=$(python ./oliveyoung/spiders/product_no_ray.py)
NO_RAY_TIME=$(echo "$NO_RAY_OUTPUT" | grep "총 소요 시간")
echo "$NO_RAY_OUTPUT" >> "$LOG_FILE"
echo "총 소요 시간 (product_no_ray.py): $NO_RAY_TIME" >> "$LOG_FILE"

# 4. MongoDB 데이터 개수 기록 후 초기화
echo "4. MongoDB 데이터 기록 및 초기화..." >> "$LOG_FILE"
DATA_COUNT_AFTER=$(mongo --quiet --eval "db.getSiblingDB('$DB_NAME').$COLLECTION_NAME.count()")
echo "현재 데이터 개수: $DATA_COUNT_AFTER" >> "$LOG_FILE"
mongo --quiet --eval "db.getSiblingDB('$DB_NAME').$COLLECTION_NAME.deleteMany({})"
echo "데이터 초기화 완료." >> "$LOG_FILE"

# 1. python ./oliveyoung/spiders/product_ray.py 실행
echo "1. product_ray.py 실행 중..." >> "$LOG_FILE"
RAY_OUTPUT=$(python ./oliveyoung/spiders/product_ray.py)
RAY_TIME=$(echo "$RAY_OUTPUT" | grep "총 소요 시간")
echo "$RAY_OUTPUT" >> "$LOG_FILE"
echo "총 소요 시간 (product_ray.py): $RAY_TIME" >> "$LOG_FILE"

# 2. MongoDB 데이터 개수 기록 후 초기화
echo "2. MongoDB 데이터 기록 및 초기화..." >> "$LOG_FILE"
DATA_COUNT_BEFORE=$(mongo --quiet --eval "db.getSiblingDB('$DB_NAME').$COLLECTION_NAME.count()")
echo "현재 데이터 개수: $DATA_COUNT_BEFORE" >> "$LOG_FILE"
mongo --quiet --eval "db.getSiblingDB('$DB_NAME').$COLLECTION_NAME.deleteMany({})"
echo "데이터 초기화 완료." >> "$LOG_FILE"

# 실험 종료 시간 기록
echo "======================" >> "$LOG_FILE"
echo "실험 종료: $(date)" >> "$LOG_FILE"

# 결과 파일명 출력
echo "실험 결과가 $LOG_FILE 에 저장되었습니다."