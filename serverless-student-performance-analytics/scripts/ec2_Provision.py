import boto3

ec2 = boto3.client(
    'ec2',
    region_name='ap-south-1'
)

response = ec2.run_instances(
    ImageId='ami-0f58b397bc5c1f2e8',  # Example Amazon Linux AMI
    InstanceType='t3.micro',
    MinCount=1,
    MaxCount=1,
    KeyName='yutube-instance1-ayush'
)

print(response)