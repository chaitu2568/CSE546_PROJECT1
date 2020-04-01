import boto3
from botocore.exceptions import NoCredentialsError
from S3_CRUD import S3
import time
from SQS_CRUD import SQS
import json

''' This program runs as a Daemon Process, and continously 
upload the recorded videos from rasberry-pi to S3 videos bucket'''

if __name__ == '__main__':

    ''' Getting the AWS Credentials from the 'login.config' file '''

    with open('login.config') as json_data_file:
        data = json.load(json_data_file)

    print("VIDEO UPLOADING DAEMON STARTED")
    s3 = S3(data['login']['UPLOADED_VIDEOS_BUCKET_NAME'])
    sqs = SQS(data['login']['UPLOAD_VIDEOS_QUEUE_NAME'])

    while True:
        time.sleep(0.2)
        name, receipt_handle = sqs.receive_messages_from_queue(1)
        if(name is not None):
            print("----------------- RECEIEVED "+name+" FROM VIDEO UPLOAD QUEUE------------------")
            try:
                print("----------------UPLOADING VIDEO FILE ",name)
                s3.upload_file_to_s3(name)
                print('')
                print('',time.time())
                print("--------------UPLOADED VIDEO ",name," SUCCESSFULLY TO S3 (VIDEOS) BUCKET-----------")
                print('')
                print('')

                ''' After Successful upload, deleting the message from SQS queue'''
                sqs.delete_message_from_queue(receipt_handle)

            except NoCredentialsError:
                print("Credentials not available", name)
            except:
                print("nmae is", name)
