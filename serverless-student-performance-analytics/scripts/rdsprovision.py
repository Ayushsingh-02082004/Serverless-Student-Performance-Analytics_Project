import boto3

rds = boto3.client('rds',region_name = 'ap-south-1')

response = rds.create_db_instance(
    DBName = 'studentdb',
    DBInstanceIdentifier = 'student-db-instance',
    AllocatedStorage = 20,
    DBInstanceClass = 'db.t3.micro',
    Engine = 'mysql',
    MasterUsername = 'admin',
    MasterUserPassword = 'Password123',
    PubliclyAccessible = True,
    StorageType = 'gp2'
)

print(response)





