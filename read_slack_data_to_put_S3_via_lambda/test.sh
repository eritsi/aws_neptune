#!/bin/sh
# CURRENT=$(cd $(dirname $0);pwd) # 絶対パス
CURRENT=$(dirname $0)
cd $CURRENT

# lambda_function.py を型から作成する
read -p "Enter Your SLACK_API_TOKEN: " SLACK_API_TOKEN
read -p "Enter Your slack channel code: " SLACK_CHANNEL_CODE
read -p "Enter Your S3 Bucket Name to store json data: " BUCKET_NAME
read -p "Enter Your json file Name (with .json): " JSON_FILE_NAME

eval "cat lambda_function_example.py | \
sed -e 's/{SLACK_API_TOKEN}/"$SLACK_API_TOKEN"/g' \
-e 's/{SLACK_CHANNEL_CODE}/"$SLACK_CHANNEL_CODE"/g' \
-e 's/{BUCKET_NAME}/"$BUCKET_NAME"/g' \
-e 's/{FILE_NAME}/"$JSON_FILE_NAME"/g' > lambda_function.py"
# cat lambda_function_example.py | \
# sed -e 's/{SLACK_API_TOKEN}/$SLACK_API_TOKEN/g' \
# -e 's/{SLACK_CHANNEL_CODE}/$SLACK_CHANNEL_CODEVCLAD0A/g' \
# -e 's/{BUCKET_NAME}/$BUCKET_NAME/g' \
# -e 's/{FILE_NAME}/$JSON_FILE_NAME/g' > lambda_function.py

# upload用のzipを作成
zip -r for_upload.zip lambda_function.py slack_sdk*
read -p "Enter Your Lambda Function Name: " AWS_LAMBDA_NAME

GET_ARN_ROLE=$(eval "aws iam list-roles --query 'Roles[?RoleName==\`"$AWS_ROLE_NAME"\`].Arn' --output text")

# lambda functionを作成
aws lambda create-function --function-name $AWS_LAMBDA_NAME \
--zip-file fileb://for_upload.zip \
--role "$GET_ARN_ROLE" \
--runtime python3.8 \
--timeout 900\
--handler lambda_function.lambda_handler
rm for_upload.zip
rm lambda_function.py