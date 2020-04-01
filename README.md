**Project1: IaaS—AmazonWebServices**

In this Project, we build an elastic and responsive application that utilizes cloud-resources and IoT devices to achieve real-time object detection on videos recorded by the devices. Specifically, we developed this application using Amazon Web Services (AWS)based cloud and Raspberry Pi based IoT.

**We implemented our project in Python 3.7**

Below information gives you the step-by-step procedure to run the Application.

**Hardware Requirements:**

1. Rasberry-Pi
2. Camera
3. Object-detection Sensor
4. Micro-SD Card

First, install Raspbian

1. Download Etcher (https://www.balena.io/etcher/), a tool for flashing OS images to SD cards, to your own host computer.
2. Download the Raspbian image
3. Flash the Raspbian image to a microSD card using Etcher
4. Plug the card to the Raspberry Pi (we will call it the Pi hereinafter) and power it up


And then integrate the Object-detection Sensor and Camera Module.

**Pre-Execution instructions:**

**IN Rasberry-Pi**
1. SSH to PI using the following command: ssh pi@'your_local_ip'
2. Download the pre-trained model weights of tiny-yolo using the following command:      wget https://pjreddie.com/media/files/yolov3-tiny.weights
3. Tranfer **all the files** in this folder to PI using the following command: scp /*enter-the-path-to-this-repo-folder/* pi@'*your-local-ip*':/home/pi/darknet
4. Make sure to run the command: **Xvfb :1 & export DISPLAY=:1** to enable x display service.
5. Install boto3
6. Now login to AWS account using the AWS credentials provided.

**Next, in EC2-Instance****

7. Create an AWS EC2 master instance (controller) and install the darknet yolo in the AWS instance using git clone https://github.com/pjreddie/darknet.git
8. Now ssh into EC2 instance using the following command, ssh -i "***path-to-pem-file***" ubuntu@'***ec2-instance-address***'
9. Now move to the darknet folder and create virtual environment using the following commands,
***1. sudo apt install virtualenv 2. virtualenv -p python3 cse546env ***
10. Now install boto3 and xvfbwrapper using following commands,
***1. pip3 install boto3  2. pip3 install xvfbwrapper ***
11. Now scp all the files in the project folder to darknet folder in EC2 master instance(controller) using the following command: scp -i /***path-to-pem-file***/ /***path-to-project-directory***/* ubuntu@'***ec2-instance-address***':/home/ubuntu/darknet
12. Now edit the 'rc.local' file using the command ***sudo vi /etc/rc.local*** and add ***bash /home/ubuntu/darknet/master.sh*** line
13. Now create the snap-shot of this EC2-master-instance and create the AMI image. 
14. Add the AMI image to EC2_CRUD.py file and then that python file scp to EC2_instance.

***Execution Instructions:***

***Descriptions of all the Program files present in the directory are mentioned in the report. Please go through them first and then perform the execution.***

1. In your PI, run the following command: ***bash run_script.sh***
2. If you manually want to run the '***LOAD_BALANCER.py***' program on EC2 controller instance then ssh to instance and run the following command on darknet folder: ***python3 LOAD_BALANCER.py***. 
else for auto-running, go to rc.local file in EC2 controller and add ***bash /home/ubuntu/darknet/LOAD_BALANCER.PY*** 
3. Make sure to run both commands simultaneously on both PI and EC2 controller to start the activity. Once the process is started, then entire flow of the project is explained in the report.
4. To kill the activity, run the following command in PI darknet folder: ***bash clean.sh***
