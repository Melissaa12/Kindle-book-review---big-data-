import boto3
from boto3 import NullHandler
import paramiko
import time
stack_name = "DBPJT3"
MongoIP = "0.0.0.0"
MySQLIP = "0.0.0.0"
WebServerIP = "0.0.0.0"
aws_access_key_id="ASIAZY6F36H2I6EPVPXH"
aws_secret_access_key="Kp1GI5eA1LFT2TamCI+6NuIq3vUyV8qa8xS1Mcbx"
aws_session_token="FwoGZXIvYXdzEEMaDEX7Mnf7Ij2XUcuzlCLVAUXYXfrvhuWd+BfrfBWkK9LZee9wodPRZuVRzTm4Fd+GD21MpBJk/ffB5zUrndIh/AvJD9T7A2ntlZMIosUE1bO39/EvCzF5bj7riwTj5BkUhthVWz2DLA4HONzi8i59wQxZyiDO3lkfSBFMdoZj+nqx58pJrTucnRIrMceNxJYcMRySKQGvwThWFhfNCN4Iyu0xBloNBGlGdCdkX810nD2ZUOAR9kuH6d4bhm9dnak03M17uS6rUWHyAta1wV9XjF3B2sKiGbvsFqxncn3YpQaBLIhQqSiC56L+BTItolCYxSO/lewzHhIlfwE7srna3N70TljFogA+J88Tk5fx4Y8cSSs6i6mDIJPc"
cloud_formation_client = boto3.client('cloudformation',aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key,aws_session_token=aws_session_token,region_name="us-east-1")

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
        if(value == "WebServerIP"):
            WebServerIP = i["OutputValue"]

def ssh_connect_with_retry(ssh, ip_address, retries):
    if retries > 3:
        return False
    privkey = paramiko.RSAKey.from_private_key_file(
        'C:/Users/Rahul/Downloads/rahuleducate1.pem')
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
ip_address =MongoIP
print("Mongo IP: " , MongoIP)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh_connect_with_retry(ssh, ip_address, 0)



stdin, stdout, stderr = ssh.exec_command("pwd")
print('stdout:', stdout.read())
print('stderr:', stderr.read())
stdin, stdout, stderr = ssh.exec_command("ls")
print('stdout:', stdout.read())
print('stderr:', stderr.read())

stdin, stdout, stderr = ssh.exec_command("wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -")
print('stdout:', stdout.read())
print('stderr:', stderr.read())
stdin, stdout, stderr = ssh.exec_command('echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list')
print('stdout:', stdout.read())
print('stderr:', stderr.read())
stdin, stdout, stderr = ssh.exec_command("sudo apt-get update")
print('stdout:', stdout.read())
print('stderr:', stderr.read())
print("###############")
stdin, stdout, stderr = ssh.exec_command("lsb_release -a")
print('stdout:', stdout.read())
print('stderr:', stderr.read())
print("###############")

stdin, stdout, stderr = ssh.exec_command("sudo apt-get install -y mongodb-org")
print('stdout:', stdout.read())
print('stderr:', stderr.read())
print("HAFDJJUFDA")
stdin, stdout, stderr = ssh.exec_command("sudo systemctl daemon-reload")
print('stdout:', stdout.read())
print('stderr:', stderr.read())
stdin, stdout, stderr = ssh.exec_command("sudo service mongod start")
print('stdout:', stdout.read())
print('stderr:', stderr.read())

stdin, stdout, stderr = ssh.exec_command("wget -c https://istd50043.s3-ap-southeast-1.amazonaws.com/meta_kindle_store.zip -O meta_kindle_store.zip")
print('stdout:', stdout.read())
print('stderr:', stderr.read())

stdin, stdout, stderr = ssh.exec_command("sudo apt install unzip")
print('stdout:', stdout.read())
print('stderr:', stderr.read())
stdin, stdout, stderr = ssh.exec_command("unzip meta_kindle_store.zip")
print('stdout:', stdout.read())
print('stderr:', stderr.read())

stdin, stdout, stderr = ssh.exec_command("mongoimport --db kindle --collection metadata --file meta_Kindle_Store.json --legacy")
print('stdout:', stdout.read())
print('stderr:', stderr.read())
'''
stdin, stdout, stderr = ssh.exec_command("sudo iptables -A INPUT -p tcp --destination-port 27017 -m state --state NEW,ESTABLISHED -j ACCEPT")
print('stdout:', stdout.read())
print('stderr:', stderr.read())
stdin, stdout, stderr = ssh.exec_command("sudo iptables -A OUTPUT  -p tcp --source-port 27017 -m state --state ESTABLISHED -j ACCEPT")
print('stdout:', stdout.read())
print('stderr:', stderr.read())
'''
'''stdin, stdout, stderr = ssh.exec_command('mongo --eval "db.createUser({user: 'rp' ,pwd:'lol' , roles: [{role: 'readWrite' , db:'kindle'}]} )"')
print('stdout:', stdout.read())
print('stderr:', stderr.read())
'''
stdin, stdout, stderr = ssh.exec_command('yes | sudo apt install python-pip' )
print('stdout:', stdout.read())
print('stderr:', stderr.read())
stdin, stdout, stderr = ssh.exec_command('pip install flask' )
print('stdout:', stdout.read())
print('stderr:', stderr.read())
stdin, stdout, stderr = ssh.exec_command('pip install pymongo' )
print('stdout:', stdout.read())
print('stderr:', stderr.read())
stdin, stdout, stderr = ssh.exec_command('pip install flask_restful' )
print('stdout:', stdout.read())
print('stderr:', stderr.read())
stdin, stdout, stderr = ssh.exec_command('echo "' + str(MySQLIP)+'" >> ip.txt' )
print('stdout:', stdout.read())
print('stderr:', stderr.read())
stdin, stdout, stderr = ssh.exec_command('sudo apt install git' )
print('stdout:', stdout.read())
print('stderr:', stderr.read())
stdin, stdout, stderr = ssh.exec_command('git clone https://github.com/Hsengiv2000/BigdataMongo.git' )
print('stdout:', stdout.read())
print('stderr:', stderr.read())
stdin, stdout, stderr = ssh.exec_command('sudo nohup python BigdataMongo/runmongo.py > log.txt 2>&1 &' )
print('stdout:', stdout.read())
print('stderr:', stderr.read())



'''
stdin, stdout, stderr = ssh.exec_command("hello")
print('stdout:', stdout.read())
print('stderr:', stderr.read())
stdin, stdout, stderr = ssh.exec_command("sudo apt-get install mysql-server")
print('stdout:', stdout.read())
print('stderr:', stderr.read())
stdin, stdout, stderr = ssh.exec_command("mysql_secure_installation")
print('stdout:', stdout.read())
'''
