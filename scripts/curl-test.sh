#!/bin/bash

for i in {1..5}; do
  echo -n "Request $i: "
  curl -s -H "X-API-Key: abc123" http://localhost:8100/api/test
  echo ""
  sleep 1
done