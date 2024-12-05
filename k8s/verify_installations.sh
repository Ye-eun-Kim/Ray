#!/bin/bash

# 클러스터의 모든 파드 이름 가져오기
HEAD_POD=$(kubectl get pods -n yek-ray -l ray.io/node-type=head -o jsonpath='{.items[0].metadata.name}')
WORKER_PODS=$(kubectl get pods -n yek-ray -l ray.io/node-type=worker -o jsonpath='{.items[*].metadata.name}')

# 설치 확인을 위한 Python 명령어
CHECK_CMD="python3 -c 'import scrapy; import twisted; import pymongo; import dns; import ray; print(\"All modules successfully imported!\")'"

# Head 노드 확인
echo "Verifying installations on head node: $HEAD_POD"
kubectl exec -it -n yek-ray $HEAD_POD -- /bin/bash -c "$CHECK_CMD"

# Worker 노드들 확인
for pod in $WORKER_PODS; do
    echo "Verifying installations on worker node: $pod"
    kubectl exec -it -n yek-ray $pod -- /bin/bash -c "$CHECK_CMD"
done

echo "All verifications completed!"