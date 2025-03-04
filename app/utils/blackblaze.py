from b2sdk.v2 import InMemoryAccountInfo, B2Api
import logging

def initialize_b2(app_key_id: str, app_key: str):
    """
    Initializes the B2 API with the provided credentials.
    """
    try:
        info = InMemoryAccountInfo()
        b2_api = B2Api(info)
        b2_api.authorize_account("production", app_key_id, app_key)
        logging.info("Backblaze B2 initialized successfully.")
        return b2_api
    except Exception as e:
        logging.error(f"Failed to initialize Backblaze B2: {e}")
        raise  # Rethrow the exception after logging it

def list_buckets(b2_api: B2Api):
    """
    Lists all buckets associated with the account.
    """
    try:
        buckets = list(b2_api.list_buckets())
        logging.info(f"Found {len(buckets)} buckets.")
        return buckets
    except Exception as e:
        logging.error(f"Failed to list buckets: {e}")
        return []

def upload_file(b2_api: B2Api, bucket_name: str, local_file_path: str, file_name_in_bucket: str):
    """
    Uploads a file to the specified bucket.
    """
    try:
        bucket = b2_api.get_bucket_by_name(bucket_name)
        with open(local_file_path, "rb") as file:
            # Instead of reading the entire file into memory, we stream it
            bucket.upload_bytes(file.read(), file_name_in_bucket)
            logging.info(f"File '{file_name_in_bucket}' uploaded successfully!")
    except Exception as e:
        logging.error(f"Error uploading file '{file_name_in_bucket}': {e}")
        raise  # Rethrow to propagate the error

def download_file(b2_api: B2Api, bucket_name: str, file_name_in_bucket: str, local_file_download_path: str):
    """
    Downloads a file from the specified bucket.
    """
    try:
        bucket = b2_api.get_bucket_by_name(bucket_name)
        file_info = bucket.download_file_by_name(file_name_in_bucket)
        file_info.save_to(local_file_download_path)
        logging.info(f"File '{file_name_in_bucket}' downloaded successfully to '{local_file_download_path}'!")
    except Exception as e:
        logging.error(f"Error downloading file '{file_name_in_bucket}': {e}")
        raise

def delete_file(b2_api: B2Api, bucket_name: str, file_name_in_bucket: str):
    """
    Deletes a file from the specified bucket.
    """
    try:
        bucket = b2_api.get_bucket_by_name(bucket_name)
        file_version = bucket.get_file_info_by_name(file_name_in_bucket)
        bucket.delete_file_version(file_version.id_, file_name_in_bucket)
        logging.info(f"File '{file_name_in_bucket}' deleted successfully!")
    except Exception as e:
        logging.error(f"Error deleting file '{file_name_in_bucket}': {e}")
        raise
