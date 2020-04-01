import os
import time
import boto3
from EC2_CRUD import EC2
import urllib.request
from SQS_CRUD import SQS
from S3_CRUD import S3
from xvfbwrapper import Xvfb
import json

" This is the Slave_Program which runs on Slave EC2 instances that are Spawned by load-balancing program" \
"running on Master Ec2 instance (controller)"

''' URL to retreive the instance-id of current running EC2 instance '''

instanceid = urllib.request.urlopen('http://169.254.169.254/latest/meta-data/instance-id').read().decode()


def result_extract(file_name,server,video_file_name):
    '''  Method to Parse the result from the Darknet Detection  '''
    result = open(file_name, 'r')
    results = result.read().split('\n')
    result.close()
    given_objs = open('/home/'+server+'/darknet/data/coco.names')
    obj_list = given_objs.read().split('\n')
    objects = []
    for word in results:
        for match in obj_list:
            if word.startswith(match) and match:
                objects.append(match)
    obj = list(set(objects))

    if len(obj) == 0:
        obj = ['NO-OBJECT-DETECTED']

    fobj = open(file_name,"w+")
    objects = ','.join(obj)
    fobj.write((video_file_name+" : "+objects))


def main():

    ''' Getting the AWS Credentials from the 'login.config' file '''

    with open('login.config') as json_data_file:
        data = json.load(json_data_file)

    sqs_obj = SQS(data['login']['VIDEO_KEYS_QUEUE_NAME'])
    ec2 = EC2()
    s3_obj_1 = S3(data['login']['UPLOADED_VIDEOS_BUCKET_NAME'])
    s3_obj_2 = S3(data['login']['RESULTS_BUCKET_NAME'])

    delete_flag = False
    while True:
        video_name, recepit_handle = sqs_obj.receive_messages_from_queue(1)
        if video_name is not None:
                delete_flag = False
                try:

                    s3_obj_1.download_file_from_s3(video_name)
                    try:

                        file_name = video_name.split(".")
                        file_name = file_name[0] + '_' + str(instanceid)+ '.txt'
                        cmd_to_det_obj = './darknet detector demo cfg/coco.data cfg/yolov3-tiny.cfg yolov3-tiny.weights '+ video_name + ' > ' + file_name
                        os.system(cmd_to_det_obj)

                        try:
                            result_extract(file_name,'ubuntu',video_name)
                            s3_obj_2.upload_file_to_s3(file_name)
                            sqs_obj.delete_message_from_queue(recepit_handle)
                        except:

                            pass

                    except FileNotFoundError:
                        pass

                    except:
                        pass
                except:
                    """This handle the Scenario, when ever the video_name_key retrieved from the SQS queue is not
                     find in the S3 bucket, so it deletes the message and send back to queue again"""
                    sqs_obj.delete_message_from_queue(recepit_handle)
                    sqs_obj.send_message_to_queue(video_name)


        elif int(sqs_obj.get_length_of_queue()) -1 <= 0:

            '''Below is the logic for Scaling-in by self-stopping the instance itself,if 
            there is no message in the queue for 60 seconds'''

            print("No of messsages in sqs are zero right now \n")
            if delete_flag:
                ''' logic to delete own instance '''
                print("stopping the instance now \n")
                ec2.stop_instance(instanceid)

            time.sleep(60)
            delete_flag = True

if __name__ == '__main__':
    vdisplay = Xvfb()
    vdisplay.start()
    main()
    vdisplay.stop()

