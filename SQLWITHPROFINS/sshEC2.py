import boto3
from boto3 import NullHandler
import paramiko
import time
import subprocess
import sys
numberOfSlaves = int(sys.argv[4])
slaveiparr = []
slavednsarr = []
stack_name = "DBPJT3"
MongoIP = "0.0.0.0"
MySQLIP = "0.0.0.0"
WebServerIP = "0.0.0.0"
cloud_formation_client = boto3.client('cloudformation',aws_access_key_id= sys.argv[1],aws_secret_access_key=sys.argv[2],aws_session_token=sys.argv[3],region_name=sys.argv[5])

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
        if(value == "MasterIP"):
            MasterIp = i["OutputValue"]
        if(value == "Slave0IP"):
            Slave0Ip = i["OutputValue"]
        if(value == "MasterPriIP"):
            MasterPriIp = i["OutputValue"]
        if(value == "Slave0PriIP"):
            Slave0PriIp = i["OutputValue"]
        for j2 in range(numberOfSlaves):
            if(value == ('Slave' + str(j2+1) +'PriIP')):
                slavednsarr.append(i["OutputValue"])
            if(value == ('Slave'+ str(j2+1)+'IP')):
                slaveiparr.append(i["OutputValue"])
slaveiparr.append("STOP")
slavednsarr.append("STOP")
print('this are the slave ipanmes' + str(slaveiparr))
print('these are the slave dns names' + str(slavednsarr))

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

# get instance
ip_address = MySQLIP
print('MYSQLIP')
print(MySQLIP)
print('MONGOIP')
print(MongoIP)
print('Master public ip')
print(MasterIp)
print('slave0 public ip')
print(Slave0Ip)
print('master private ip')
print(MasterPriIp)
print('secondary private ip')
print(Slave0PriIp)






#Setting up MongoDB server
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

#setting up sql server
subprocess.call(['bash','sqlbash.sh',MySQLIP,'key.pem'])



#Setting up Data Analytics Server
passingtosub = ['bash','databash.sh','key.pem',MasterIp,MasterPriIp,Slave0Ip,Slave0PriIp]
for i in range(len(slavednsarr)):
    passingtosub.append(slaveiparr[i])
    passingtosub.append(slavednsarr[i])
subprocess.call(passingtosub)


# Setting up the Webserver
print("SQLPublicIP")
print(MySQLIP)
print("MONGOPublicIP")
print(MongoIP)
print("WEBSERVERIP")
print(WebServerIP)
subprocess.call(['bash','websetup.sh',WebServerIP,'key.pem',MongoIP,MySQLIP,MasterIp])