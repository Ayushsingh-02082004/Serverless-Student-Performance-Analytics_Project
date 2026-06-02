import boto3

dynamodb = boto3.client(
'dynamodb',
region_name = 'ap-south-1',
)


response = dynamodb.create_table(
TableName = 'Students',

KeySchema = [{
'AttributeName' : 'StudentId',
'KeyType' : 'HASH'
}],

AttributeDefinitions= [{
'AttributeName':'StudentId',
'AttributeType': 'S'
}],

BillingMode = 'PAY_PER_REQUEST'

)
print(response)
