import boto3

bucket = 'nmlab-final-mecoli1219'
s3 = boto3.client('s3')

with open("./tsungnan-1.jpg", 'rb') as image:
    print(image)
    s3.upload_fileobj(image, bucket, "owner.jpg")