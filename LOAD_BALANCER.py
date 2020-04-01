from EC2_CRUD import EC2
from SQS_CRUD import SQS
import json
import time

def load_balancing():

    ''' Getting the AWS Credentials from the 'login.config' file '''

    with open('login.config') as json_data_file:
        data = json.load(json_data_file)

    sqs_video = SQS(data['login']['VIDEO_KEYS_QUEUE_NAME'])
    ec2 = EC2()

    while True:

        sqs_length = int(sqs_video.get_length_of_queue()) + int(sqs_video.get_number_of_flight_messages())-1
        running_number = ec2.get_current_running_instances_number()-1
        dummy_sqs = sqs_length
        dummy_running = running_number


        print('sqs_length_is',sqs_length, " running are", running_number)

        if sqs_length>running_number and sqs_length > 0:

            '''STARTING THE STOPPED INSTANCES'''

            print(running_number, " running are in loop", sqs_length)
            stopped_number,stopped_instances = ec2.current_stopped_instances()
            for ins in stopped_instances:
                if(dummy_sqs <= dummy_running):
                    break
                ec2.start_instance(ins.id)
                print('-----starting insannce----', ins.id)
                dummy_running = dummy_running+1

            while(dummy_sqs  > dummy_running):

                '''WHEN MAXIMUM NUMBER OF FREE-TIER INSTANCES ARE REACHED, IT WILL NOT ALLOW FURTHER
                TO CREATE THE NEW EC2 INSTANCES'''

                if dummy_running == 9:
                    break
                print("--------creating instances-------- ", dummy_running, sqs_length)
                ec2.create_EC2_Instance(1)
                print("------instance creation done-------")
                dummy_running = dummy_running + 1

            print("------waiting for instances to start-----")
            while(dummy_running != running_number):
                print(running_number,dummy_running)
                running_number = ec2.get_current_running_instances_number()-1

        time.sleep(2)


if __name__ == '__main__':
    load_balancing()
