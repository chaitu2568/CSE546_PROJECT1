import boto3
import json

class S3:

    def __init__(self,bucket_name):

        ''' Getting the AWS Credentials from the 'login.config' file '''

        with open('login.config') as json_data_file:
            data = json.load(json_data_file)

        self.access_key = data['login']['ACCESSKEY']
        self.secret_key = data['login']['SECRETKEY']
        self.session_token = data['login']['TOKEN']

        self.s3_resource = boto3.resource('s3',region_name="us-east-1",
                             aws_access_key_id=self.access_key,
                             aws_secret_access_key=self.secret_key,
                            aws_session_token= self.session_token
                                           )
        self.s3_client = boto3.client('s3',region_name="us-east-1",
                             aws_access_key_id=self.access_key,
                             aws_secret_access_key=self.secret_key,
                            aws_session_token= self.session_token
                                           )
        self.bucket_name = bucket_name

    ''' Method to upload the file to S3 bucket'''

    def upload_file_to_s3(self,name_of_file):
        print("Uploading the File: ",name_of_file)
        self.s3_client.upload_file(name_of_file, self.bucket_name, name_of_file)
        print(name_of_file,": Upload successfull")

    ''' Metohd to download the file from S3 bucket '''

    def download_file_from_s3(self,name_of_file):
        print("Downloading the File: ",name_of_file)
        name_of_downloaded_file = name_of_file
        self.s3_client.download_file(self.bucket_name, name_of_file , name_of_downloaded_file)
        print(name_of_file,": Download successfull")


if __name__ == '__main__':
    # obj = S3()
    pass



