import boto3
import sys
import time
import os
import json



class EC2:

    def __init__(self):

        ''' Getting the AWS Credentials from the 'login.config' file '''

        with open('login.config') as json_data_file:
            data = json.load(json_data_file)

        self.access_key = data['login']['ACCESSKEY']
        self.secret_key = data['login']['SECRETKEY']
        self.session_token = data['login']['TOKEN']

        self.ec2_resource = boto3.resource('ec2',region_name="us-east-1",
                             aws_access_key_id=self.access_key,
                             aws_secret_access_key=self.secret_key,
                            aws_session_token= self.session_token
                                           )
        self.ec2_client = boto3.client('ec2',region_name="us-east-1",
                             aws_access_key_id=self.access_key,
                             aws_secret_access_key=self.secret_key,
                            aws_session_token= self.session_token
        )

    ''' Method to Create a New EC2 Instance '''

    def create_EC2_Instance(self, no_of_instances):

        '''Below logic creates the Pem file new instance created or use the exisiting one'''

        ec2 = self.ec2_resource
        if os.path.isfile('TestKeys_2.pem'):
            print ("File exist using TestKeys_2 to create instances")
        else:
            outfile = open('TestKeys_2.pem','w')
            key_pair = ec2.create_key_pair(KeyName='TestKeys_2')
            KeyPairOut = str(key_pair.key_material)
            outfile.write(KeyPairOut)

        instances = ec2.create_instances(
             ImageId='ami-08cff570077cf46af',
             MinCount=no_of_instances,
             MaxCount=no_of_instances,
             InstanceType='t2.micro',
             KeyName='TestKeys_2'
        )

    ''' Method to retrieve no of instances initiated '''

    def get_number_of_instances(self):
        for ins in self.ec2_resource.instances.all():
            print(ins.id)

    def get_instance_id(self, instance):
        return instance.id

    ''' Method to give the current state of instances '''

    def get_current_stateof_instance(self,instance_id):
        for insta in self.ec2_resource.instances.filter(Filters=[{'Name':'instance-id','Values':[instance_id]}]):
            ans = insta.state['Name']
        return ans

    ''' Method to give information about current number of running instances '''

    def current_running_instances(self):
        instances = self.ec2_resource.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
        for instance in instances:
            print(instance.id, instance.instance_type)

    ''' Method to give current number of running instances '''

    def get_current_running_instances_number(self):
        instances = self.ec2_resource.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
        count = 0
        for instance in instances.all():
            count += 1
        return count

    def get_current_total_instances_number(self):
        instances = self.ec2_resource.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running','stopped']}])
        count = 0
        for instance in instances.all():
            count += 1
        return count

    ''' Method to give information about current number of stopped instances '''

    def current_stopped_instances(self):
        instances = self.ec2_resource.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])
        count = 0
        for instance in instances.all():
            count += 1
        return count, instances

    ''' Method to start a new instance '''

    def start_instance(self,instance_id):
        current_state = self.get_current_stateof_instance(instance_id)

        if current_state == 'running':
            print('Instance is running already')

        else:
            for insta in self.ec2_resource.instances.filter(Filters = [{'Name':'instance-id','Values':[instance_id]}]):
                insta.start()
                # print('Instance is going to Start, Will let you Know Once it is Started')
                # insta.wait_until_running()
                # print('Instance is Running Now')

    ''' Method to stop a running instance '''

    def stop_instance(self,instance_id):
        current_state = self.get_current_stateof_instance(instance_id)

        if current_state == 'stopped':
            print('Instance is stopped already')

        else:
            for insta in self.ec2_resource.instances.filter(Filters = [{'Name':'instance-id','Values':[instance_id]}]):
                insta.stop()
                print('Instance is going to stop, Will let you Know Once it is Stopped')
                insta.wait_until_stopped()
                print('Instance is Stopped Now')

    ''' Method a create EBS snapshot'''

    def create_snapshot(self, instance_volume):
        snapshot = self.ec2_resource.create_snapshot(VolumeId=instance_volume, Description='description')
        return snapshot

    """ Method to create an Instance from the Image created using Snapshot"""

    def attach_snapshot_to_instance(self,snapshot,instance_id):
        volume = self.ec2_resource.create_volume(SnapshotId=snapshot.id, AvailabilityZone='us-east-1')
        self.ec2_resource.Instance(instance_id).attach_volume(VolumeId=volume.id, Device='/dev/sdy')
        snapshot.delete()


if __name__ == '__main__':
    obj = EC2()
    obj.create_EC2_Instance(1)
    




