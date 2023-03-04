from inspect import Attribute
import boto3

bucket = 'nmlab-final-mecoli1219'
client = boto3.client('rekognition')
s3 = boto3.client('s3')


# response = client.detect_faces(
#     Image={
#         'S3Object': {
#             'Bucket': bucket,
#             'Name': 'owner.jpg',
#         },
#     }
# )

# print(response['FaceDetails'])

# print("----------------------------------------------------")


# response = client.compare_faces(
#     SourceImage={
#         'S3Object': {
#             'Bucket': bucket,
#             'Name': 'owner.jpg',
#         },
#     },
#     TargetImage={
#         'S3Object': {
#             'Bucket': bucket,
#             'Name': 'tsungnan-2.jpg',
#         },
#     },
#     SimilarityThreshold=80,
# )

# print(response['FaceMatches'])

# print("----------------------------------------------------")
response = client.compare_faces(
    SourceImage={
        'S3Object': {
            'Bucket': bucket,
            'Name': 'test-1.jpg',
        },
    },
    TargetImage={
        'S3Object': {
            'Bucket': bucket,
            'Name': 'test-2.jpg',
        },
    },
    SimilarityThreshold=80,
)

print(response['FaceMatches'])