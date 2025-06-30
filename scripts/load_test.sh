#!/bin/bash

TARGET_URL="http://<MINIKUBE_IP>:<NODEPORT>/api"

while true; do
  curl -s $TARGET_URL > /dev/null
  sleep 0.1
done
