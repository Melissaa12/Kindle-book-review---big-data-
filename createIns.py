import boto3
session = boto3.session.Session(aws_access_key_id='ASIA2BUDARD2X6KJHHVR',
aws_secret_access_key='u4Ez8B/6I7j4Gr2NTq7UFMYwoLtn+1AIIvrnQgjL', aws_session_token='FwoGZXIvYXdzEBIaDAdbeeUbWJoiYXQR8iLKATxN78+xNZHDdbYbKFY/+ORsNR7A+TXph08CPd23uReBFBaF33pkdOkzhMGdxHDaxZYMlwYFD7iZG0zkf1SU8bQWu6jjjXQwVngnXdRVhCIWYPWs1wJDLjiaTGl2q8N2DYeIfJrafFNVOXTRFxuR5Dswrh4cyuFZVdcT+rvTVqFXgGOPNXxNgU/KVCrF6JbDk0eSTzrSq56wQAWUx3OQH/aSHG3yc0X2DPkX9yolupSEUCDpYAu+W4+wsBsI5RStCzEazMerREOqeRYoopXv/AUyLYd/MWUAwhi67H4HPQcaiYuqPA6gCgIO7U2AaMhL+J333bWs7nAl7E134B9iXw==',
region_name='us-east-1')
ec2 = session.resource('ec2')
instances = ec2.create_instances(
	ImageId = 'ami-0f82752aa17ff8f5d',
	MinCount=1,
	MaxCount=1,
	InstanceType='t2.medium',
	KeyName='dbproject')