#!/bin/bash

while true
do
  POD=$(kubectl get pods -l app=my-app -o jsonpath="{.items[0].metadata.name}")
  echo "Deleting pod: $POD"
  kubectl delete pod $POD
  sleep 10
done
