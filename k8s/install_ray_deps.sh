#!/bin/bash

# 클러스터의 모든 파드 이름 가져오기
HEAD_POD=$(kubectl get pods -n yek-ray -l ray.io/node-type=head -o jsonpath='{.items[0].metadata.name}')
WORKER_PODS=$(kubectl get pods -n yek-ray -l ray.io/node-type=worker -o jsonpath='{.items[*].metadata.name}')

# Head 노드 설치
echo "Installing dependencies on head node: $HEAD_POD"
kubectl exec -it -n yek-ray $HEAD_POD -- /bin/bash -c "pip install scrapy==2.8.0 Twisted==22.10.0 pymongo==4.10.1 dnspython==2.6.1 ray[client]==2.9.0"

# Worker 노드들 설치
for pod in $WORKER_PODS; do
    echo "Installing dependencies on worker node: $pod"
    kubectl exec -it -n yek-ray $pod -- /bin/bash -c "pip install scrapy==2.8.0 Twisted==22.10.0 pymongo==4.10.1 dnspython==2.6.1 ray[client]==2.9.0"
done

echo "All installations completed!"