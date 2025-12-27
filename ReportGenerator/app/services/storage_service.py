import boto3
from botocore.exceptions import ClientError
from app.database import S3_ACCESS_KEY, S3_SECRET_KEY, S3_ENDPOINT, S3_BUCKET_NAME, S3_REGION
import logging

logger = logging.getLogger(__name__)

class StorageService:
    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=S3_ENDPOINT,
            aws_access_key_id=S3_ACCESS_KEY,
            aws_secret_access_key=S3_SECRET_KEY,
            region_name=S3_REGION
        )
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        try:
            self.s3_client.head_bucket(Bucket=S3_BUCKET_NAME)
        except ClientError:
            try:
                self.s3_client.create_bucket(Bucket=S3_BUCKET_NAME)
                logger.info(f"Created bucket {S3_BUCKET_NAME}")
            except Exception as e:
                logger.error(f"Failed to create bucket: {e}")

    def upload_file(self, file_path: str, object_name: str, content_type: str = "application/pdf") -> str:
        """Upload a file to an S3 bucket and return the URL."""
        try:
            self.s3_client.upload_file(
                file_path,
                S3_BUCKET_NAME,
                object_name,
                ExtraArgs={'ContentType': content_type}
            )
            # Generate a presigned URL or public URL depending on requirements
            # For this internal service, we might just return the S3 path or a presigned URL
            
            # Generating presigned URL valid for 1 hour by default
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': S3_BUCKET_NAME, 'Key': object_name},
                ExpiresIn=3600
            )
            return url
        except ClientError as e:
            logger.error(f"Error uploading file: {e}")
            raise e
