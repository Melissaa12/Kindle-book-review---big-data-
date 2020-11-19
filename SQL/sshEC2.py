import boto3
from boto3 import NullHandler
import paramiko
import time
import subprocess
import sys
stack_name = "DBPJT3"
MongoIP = "0.0.0.0"
MySQLIP = "0.0.0.0"
WebServerIP = "0.0.0.0"

cloud_formation_client = boto3.client('cloudformation',aws_access_key_id= sys.argv[1],aws_secret_access_key=sys.argv[2],aws_session_token=sys.argv[3],region_name="us-east-1")

response = cloud_formation_client.describe_stacks(
    StackName=stack_name
)
print(response)
output = response['Stacks'][0]['Outputs']

for i in output:
    for key,value in i.items():
        if(value == "MongoIP"):
            MongoIP = i["OutputValue"]
        if(value == "MySQLIP"):
            MySQLIP = i["OutputValue"]
        if(value == "WebIP"):
            WebServerIP = i["OutputValue"]

def ssh_connect_with_retry(ssh, ip_address, retries):
    if retries > 3:
        return False
    privkey = paramiko.RSAKey.from_private_key_file(
        sys.argv[4])
    interval = 5
    try:
        retries += 1
        print('SSH into the instance: {}'.format(ip_address))
        ssh.connect(hostname=ip_address,
                    username='ubuntu', pkey=privkey)
        return True
    except Exception as e:
        print(e)
        time.sleep(interval)
        print('Retrying SSH connection to {}'.format(ip_address))
        ssh_connect_with_retry(ssh, ip_address, retries)

# get your instance ID from AWS dashboard

# get instance
ip_address = MySQLIP
print(MySQLIP)
# ssh = paramiko.SSHClient()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# ssh_connect_with_retry(ssh, ip_address, 0)

# stdin, stdout, stderr = ssh.exec_command("sudo apt-get update")
# # stdin, stdout, stderr = ssh.exec_command("echo 'y'")
# print('stdout:', stdout.read())
# print('stderr:', stderr.read())

# # stdin, stdout, stderr = ssh.exec_command("sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password '")
# # # stdin, stdout, stderr = ssh.exec_command("echo 'y'")
# # print('stdout:', stdout.read())
# # print('stderr:', stderr.read())

# # stdin, stdout, stderr = ssh.exec_command("sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password '")
# # # stdin, stdout, stderr = ssh.exec_command("echo 'y'")
# # print('stdout:', stdout.read())
# # print('stderr:', stderr.read())

# stdin, stdout, stderr = ssh.exec_command("yes Y |sudo apt install mysql-server")
# # stdin, stdout, stderr = ssh.exec_command("echo 'y'")
# print('stdout:', stdout.read())
# print('stderr:', stderr.read())


# stdin, stdout, stderr = ssh.exec_command("sudo systemctl start mysql")
# # stdin, stdout, stderr = ssh.exec_command("echo 'y'")
# print('stdout:', stdout.read())
# print('stderr:', stderr.read())
# subprocess.call(['bash','sqlbash.sh',MySQLIP,sys.argv[4]])
# setting up the web server
print(MongoIP)
print("hi")
print(WebServerIP)
subprocess.call(['bash','websetup.sh',WebServerIP,sys.argv[4]])
