from decouple import config
import boto3
from fastapi import HTTPException, status


class S3Service:
    def __init__(self):
        self.key = config('AWS_ACCESS_KEY_ID')
        self.secret = config('AWS_ACCESS_SECRET_KEY')
        self.region_name = config('AWS_S3_BUCKET_REGION')
        self.s3 = boto3.client("s3", aws_access_key_id=self.key, aws_secret_access_key=self.secret,
                               region_name=self.region_name, )
        self.bucket_name = config('AWS_S3_BUCKET_NAME')

    def upload_image(self, path: str, file_name: str, ext: str) -> str:
        try:
            self.s3.upload_file(path, self.bucket_name, file_name,
                                ExtraArgs={'ACL': 'public-read', 'ContentType': f'image/{ext}'})
            return f"https://{self.bucket_name}.s3.{self.region_name}.amazonaws.com/{file_name}"
        except Exception as ex:
            # log the exception
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, 'S3 is not available')
