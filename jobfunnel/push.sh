#!/bin/bash
rm -rf build.zip
cd ../
docker rm jobscraper
docker build -t jobscraper .
docker create -ti --name jobscraper jobscraper bash
docker cp jobscraper:/home/ubuntu/build.zip .
aws s3 cp build.zip s3://job-scraper/build.zip
aws lambda update-function-code --region "us-east-1" --function-name "JobScraper" --s3-bucket job-scraper --s3-key build.zip

# if [ $? -eq 0 ]; then
#  regions=( "us-east-1" "us-east-2" "us-west-1" "us-west-2" "ap-south-1"
#       "ap-northeast-2" "ap-southeast-1" "ap-southeast-2" "ap-northeast-1"
#       "ca-central-1" "eu-central-1" "eu-west-1" "eu-west-2" "eu-west-3" "sa-east-1" )
#     for i in "${regions[@]}"
#     do
#         aws lambda update-function-code --region $i --function-name "$1" --zip-file fileb://build.zip
#         if [ $? -eq 1 ]; then
#             return 1
#         fi
#     done 
# fi