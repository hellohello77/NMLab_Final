import boto3, base64

class AWSClient:
    def __init__(self):
        self.owner = 'owner.jpg'
        self.bucket = 'nmlab-final-mecoli1219'
        self.client = boto3.client('rekognition')
        self.s3 = boto3.client('s3')
        self.count = 0
        self.max = 30

    def getOwner(self):
        return self.s3.get_object(Bucket=self.bucket, Key=self.owner)['Body'].read()

    def getAllWeirdPeople(self):
        result = []
        for i in range(self.max):
            try:
                if i==self.count:
                    continue
                key = "test-" + str(i) + '.jpg'
                s3Object = self.s3.get_object(Bucket=self.bucket, Key=key)
                # print(s3Object['LastModified'])
                result.append([base64.b64encode(s3Object['Body'].read()).decode(), s3Object['LastModified']])
            except:
                continue
        result.sort(key=lambda s : s[1], reverse=True)
        # print(result)
        return result

    def changeOwner(self, img):
        self.uploadImage(img, self.owner)

    def uploadImage(self, img, name):
        self.s3.upload_fileobj(img, self.bucket, name)

    def compare(self, img):
        img_name = 'test-' + str(self.count) + '.jpg'
        self.uploadImage(img, img_name)

        response = self.client.detect_faces(
            Image={
                'S3Object': {
                    'Bucket': self.bucket,
                    'Name': img_name,
                },
            }
        )
        if len(response['FaceDetails']) == 0:
            self.count += 1
            if self.count >= self.max:
                self.count = 0
            return False

        response = self.client.detect_faces(
            Image={
                'S3Object': {
                    'Bucket': self.bucket,
                    'Name': 'owner.jpg',
                },
            }
        )
        if len(response['FaceDetails']) == 0:
            return False

        response = self.client.compare_faces(
            SourceImage={
                'S3Object': {
                    'Bucket': self.bucket,
                    'Name': self.owner,
                },
            },
            TargetImage={
                'S3Object': {
                    'Bucket': self.bucket,
                    'Name': img_name,
                },
            },
            SimilarityThreshold=80,
        )
        if len(response['FaceMatches']) == 0:
            self.count += 1
            if self.count >= self.max:
                self.count = 0
            return False

        return True

if __name__ == "__main__":
    awsClient = AWSClient()
    images = awsClient.getAllWeirdPeople()
    # print(images[0][1])
