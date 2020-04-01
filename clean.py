import boto3
# import Record_video
import os
import time
from botocore.exceptions import NoCredentialsError
from threading import Thread
import RPi.GPIO as GPIO
import time
from SQS_CRUD import SQS
from S3_CRUD import S3
import json
from boto3.session import Session

''' METHOD WHICH DELETES ALL THE MESSAGES FROM THE QUEUE '''

with open('login.config') as json_data_file:
     data = json.load(json_data_file)

sqs = SQS(data['login']['VIDEO_KEYS_QUEUE_NAME'])
sqs_upload = SQS(data['login']['UPLOAD_VIDEOS_QUEUE_NAME'])
sqs.clear_all_messages()
sqs_upload.clear_all_messages()
