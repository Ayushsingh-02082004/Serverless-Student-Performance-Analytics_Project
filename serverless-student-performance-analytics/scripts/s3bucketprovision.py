import boto3

s3 = boto3.client( 's3' , region_name = 'ap-south-1')


response = s3.create_bucket(
Bucket = 'ayush-student-data-bucket-12345',
CreateBucketConfiguration = {
'LocationConstraint' : 'ap-south-1'
})

print("Bucket Created")

response = s3.list_buckets()

for bucket in response['Buckets']:
    print(f"Bucket Name:  {bucket["Name"]}")
    object_reponse = s3.list_objects_v2(Bucket=bucket["Name"])
    if "Contents" in object_reponse:
        for obj in object_reponse["Contents"]:
            if not obj["Key"].endswith("/"):
                print(obj["Key"])
    