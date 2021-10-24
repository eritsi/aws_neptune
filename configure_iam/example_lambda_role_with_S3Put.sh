#!/bin/sh

if [ $# != 2 ]; then
    echo "not enough argument..."
    read -p "Enter Your Role Name: " AWS_ROLE_NAME
    read -p "Enter Your Policy Name: " AWS_S3POLICY_NAME
else
    AWS_ROLE_NAME=$1
    AWS_S3POLICY_NAME=$2
fi

aws iam create-role --role-name $AWS_ROLE_NAME --assume-role-policy-document file://policyDocument_lambda.json
aws iam create-policy --policy-name $AWS_S3POLICY_NAME --policy-document file://policyDocument_s3put.json
aws iam list-policies --scope Local | grep -5 $AWS_S3POLICY_NAME
ARN_S3=$(eval "aws iam list-policies --query 'Policies[?PolicyName==\`"$AWS_S3POLICY_NAME"\`].Arn' --output text")
aws iam attach-role-policy --role-name $AWS_ROLE_NAME --policy-arn $ARN_S3
