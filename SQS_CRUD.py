import boto3
import json

class SQS:

    def __init__(self, queue_name):

        ''' Getting the AWS Credentials from the 'login.config' file '''

        with open('login.config') as json_data_file:
            data = json.load(json_data_file)

        self.access_key = data['login']['ACCESSKEY']
        self.secret_key = data['login']['SECRETKEY']
        self.session_token = data['login']['TOKEN']

        self.queue_name = queue_name
        self.sqs_resource = boto3.resource('sqs',region_name="us-east-1",
                             aws_access_key_id=self.access_key,
                             aws_secret_access_key=self.secret_key,
                            aws_session_token= self.session_token
                                           )
        self.sqs_client = boto3.client('sqs',region_name="us-east-1",
                             aws_access_key_id=self.access_key,
                             aws_secret_access_key=self.secret_key,
                            aws_session_token= self.session_token
                                           )

    ''' Method to get the url of requested SQS queue'''

    def get_queue_url(self):
        return self.sqs_resource.get_queue_by_name(QueueName=self.queue_name).url

    ''' Method to send the messages to the Queue '''

    def send_message_to_queue(self, message):
        print("Sending the Video File Key to Queue", self.queue_name)
        response = self.sqs_client.send_message(
            QueueUrl= self.get_queue_url(),
            MessageBody=(
              message
            ),
        )
        print("Video File Sent Successfully to SQS", self.queue_name)

    ''' Method to receive the Messages from the queue '''

    def receive_messages_from_queue(self, no_of_messages):

        '''Messages are received based on the number of messages requested by the user'''

        print("Receiving the Message From the Queue", self.queue_name)

        response = self.sqs_client.receive_message(
            QueueUrl=self.get_queue_url(),
            AttributeNames=[
                'SentTimestamp'
            ],
            MaxNumberOfMessages=no_of_messages,
            MessageAttributeNames=[
                'All'
            ],
            )

        if 'Messages' not in response:
            return None,None
        try:
            print("Message Received is: ",response['Messages'][0]['Body'])
            return response['Messages'][0]['Body'],response['Messages'][0]['ReceiptHandle']
        except:
            return None,None


    ''' Method to retrieve the delete the Message from the queue'''

    def delete_message_from_queue(self,receipt_handle):

        '''To delete the Message, we should require the receipt-handle of the particular message'''

        response = self.sqs_client.delete_message(
            QueueUrl = self.get_queue_url(),
            ReceiptHandle = receipt_handle
            )
        print("Message Deleted Successfully", self.queue_name)

    ''' Method to delete all the messages from the queue '''

    def clear_all_messages(self):
        self.sqs_client.purge_queue(QueueUrl=self.get_queue_url())

    ''' Method to retrieve the no of messages in Flight '''

    def get_number_of_flight_messages(self):
        response = self.sqs_client.get_queue_attributes(
            QueueUrl=self.get_queue_url(),
            AttributeNames=['ApproximateNumberOfMessagesNotVisible']
            )
        return response['Attributes']['ApproximateNumberOfMessagesNotVisible']

    ''' Method to give approximate number of messages present in Queue excludes Flight messages'''

    def get_length_of_queue(self):
        response = self.sqs_client.get_queue_attributes(
            QueueUrl=self.get_queue_url(),
            AttributeNames=['ApproximateNumberOfMessages']
            )
        return response['Attributes']['ApproximateNumberOfMessages']


if __name__ == '__main__':
    pass








