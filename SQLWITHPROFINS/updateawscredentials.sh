#!/bin/bash
echo enter your aws_access_key_id
read access_key_id
echo enter your aws_secret_access_key
read aws_secret_access_key
echo enter your aws_session_token
read aws_session_token
echo please enter your aws region
read region

sudo tee /etc/environment <<EOF
ACCESS_KEY_ID=${access_key_id}
AWS_SECRET_ACCESS_KEY=${aws_secret_access_key}
AWS_SESSION_TOKEN=${aws_session_token}
REGION=${region}
EOF