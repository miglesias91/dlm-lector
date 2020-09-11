#!/bin/sh
export GOOGLE_APPLICATION_CREDENTIALS="/home/ec2-user/auth/dlm-lector-gcloud.json"
source /home/ec2-user/repos/dlm-lector/env/bin/activate
cd /home/ec2-user/repos/dlm-lector/
env/bin/python3 ./dlm.py --leer
