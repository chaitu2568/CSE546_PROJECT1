import boto3
import os
from threading import Thread
import RPi.GPIO as GPIO
import time
from SQS_CRUD import SQS
from S3_CRUD import S3
import psutil
import json
# import redis


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN)

video_name = 'ourvideo_'

with open('login.config') as json_data_file:
    data = json.load(json_data_file)



def trigger_camera(number):

    '''This method is used to record the video for 5 seconds'''

    name = video_name + str(number) + ".h264"
    cmd_to_cap_vid = 'raspivid -o ' + name + ' -t 5000'
    os.system(cmd_to_cap_vid)
    print(name,':-----------VIDEO_RECORDING_DONE------------')
    return name



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
    fobj.write((video_file_name+":"+objects))


''' METHOD TO PERFORM DARKNET DETECTION ON RASPI'''

def detect(name):

    '''This method is initialized by the 'detect-thread' only when 'rasberry-pi' performs the object detection,
    And this thread is triggered only when the SQS queue length is one (or) when rasberry-pi completes the current
     detection'''


    sqs = SQS(data['login']['VIDEO_KEYS_QUEUE_NAME'])
    s3 = S3(data['login']['RESULTS_BUCKET_NAME'])
    print("-------Starting the Detection-------")

    while True:
        time.sleep(0.2)
        name, recepit_handle = sqs.receive_messages_from_queue(1)
        
        if name is not None:
            print("-----Detecting Video Name -----",name)
            try:
                print("detecting file")
                file_name = name.split(".")
                file_name = file_name[0] + '.txt'
                cmd_to_det_obj = './darknet detector demo cfg/coco.data cfg/yolov3-tiny.cfg yolov3-tiny.weights '+ name + ' > ' + file_name
                os.system(cmd_to_det_obj)
                print(file_name," :---------DETECTTION_SUCCESSFULL--------------")
                sqs.delete_message_from_queue(recepit_handle)
                try:
                    result_extract(file_name ,'pi',name)
                    print("uploading the text result",file_name)
                    s3.upload_file_to_s3(file_name)
                    
                    print("-----------UPLOADED TEXT RESULT SUCESSFULLY:----------", file_name)

                except:
                    print("upload file not found")

            except FileNotFoundError:
                print("The file was not found")


if __name__ == '__main__':

    trigger_video_number = 1
    sqs = SQS(data['login']['VIDEO_KEYS_QUEUE_NAME'])
    sqs_upload = SQS(data['login']['UPLOAD_VIDEOS_QUEUE_NAME'])

    ''' Initializing and Starting the Detect thread '''
    detect_thread = Thread(target=detect, args=('bb',))
    detect_thread.start()

    try:
        print("-------STABILIZING_THE_SENSOR---------")
        time.sleep(5)
        print("---------SENSOR_STABILIZED----------")

        while trigger_video_number <= 10:
            if GPIO.input(26):
                name = trigger_camera(trigger_video_number)
                print("")
                print("")
                print("----------VIDEO_RECORDING----------: " ,trigger_video_number)
                print("")
                print("")
                trigger_video_number += 1

                ''' Starting the Computation'''
                print('---------RASPI_LOAD------------: ',int(psutil.cpu_percent()))

                '''Triggering AMAZON-WEB-SERVICES IF CPU load goes beyond threshold'''

                print(name, '-------uploaded to detect SQS queue--------')
                sqs_upload.send_message_to_queue(name)
                sqs.send_message_to_queue(name)
                print(name, '---------uploaded to upload queue-------')

    except:
        print("clean up")
        GPIO.cleanup()



