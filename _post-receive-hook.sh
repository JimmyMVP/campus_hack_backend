#!/bin/bash
path_service="/home/rinder/nodejs/rinder-backend/"

echo "======= STOP API SERVICE ======="
svc -d ~/service/rinder-backend

echo "========= GIT CHECKOUT ========="
GIT_WORK_TREE=$path_service git checkout -f master

cd $path_service
pip install -requirements.txt

echo "====== START API SERVICE ======="
svc -u ~/service/rinder-backend

echo "============= DONE ============="
