#!/usr/bin/env bash
set -o nounset
set -o errexit

for c in `docker container ls --format '{{.Names}}' --filter 'label=gatling'`
do
  echo ${c} `docker exec ${c} bash -c 'echo ""$USERS""'` `docker exec ${c} bash -c 'echo ""$SIM_NAME""'`
done