#!/bin/sh
CURRENT=$(cd $(dirname $0);pwd)

if [ $# != 2 ]; then
    echo "not enough argument..."
    read -p "Enter Your Role Name: " AWS_ROLE_NAME
    read -p "Enter Your Policy Name: " AWS_S3POLICY_NAME
else
    AWS_ROLE_NAME=$1
    AWS_S3POLICY_NAME=$2
fi

aws iam detach-role-policy --role-name $AWS_ROLE_NAME --policy-arn $ARN_S3
aws iam delete-role --role-name $AWS_ROLE_NAME
aws iam delete-policy --policy-name $AWS_S3POLICY_NAME

