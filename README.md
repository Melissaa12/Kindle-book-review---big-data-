# DBProject GROUP20
Term 6 Database Project Kindle 

# INSTRUCTIONS TO RUN

1)set up a fresh aws of ami-id: ami-0f82752aa17ff8f5d

2)```ssh ubuntu@<publicip> -i <keypempath>```
  
3)```sudo apt-get update```

4)``` sudo apt-get install git```

5)```git clone https://dbgroup202020:dbprojectpassword@github.com/ryangen97/DBProject.git```

6)```cd DBProject```

7)```cd SQLWITHPROFINS```

8)```sh dependencies.sh```

9)``` . venv/bin/activate```

10)```sh createEC2.sh```

11) #Enter AWS Credentials#



# TEARDOWN

## DELETE STACK

1)```source /etc/environment```

2)``` . venv/bin/activate```

3)```python3 deletestack.py $ACCESS_KEY_ID $AWS_SECRET_ACCESS_KEY $AWS_SESSION_TOKEN $REGION 'newawskey'```

## ONLY SHUTDOWN HADOOP

1)```sh shutdownhadoopcluster.sh $MASTERIP```
##


## To update aws credentials in the case of credential expiry
Note if either doesnt work it could be due to the aws credentials being expired(especially aws educate)

1)```sh updateawscredentials.sh```
 
2)```enter your updated credentials```
 
3)```source /etc/environment```

## To access Webpage
enter this into your browser WEBIPpublicIPaddress:3306
  
(This is generated and indicated near the end of the terminal headed by 'please enter this into your browser')

### OTHER COMMENTS
if you exited the web flask server and want to start it again, you need to ensure port connection are cleared with

```fuser -k 3306/tcp```
