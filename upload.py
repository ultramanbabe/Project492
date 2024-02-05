#!/usr/bin/python3

import os 
from google.cloud import storage
from firebase_admin import credentials, initialize_app

#service_account_key_path = '/home/pi/project492/ServiceAccountKey.json'
service_account_key_path = '/home/pi/project492/ServiceAccountKey_appEngineDefault.json' 
local_images_folder = '/home/pi/project492/images/'
remote_images_folder = 'https://project492-9a253.appspot.com/images' 
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '/home/pi/project492/ServiceAccountKey.json'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '/home/pi/project492/ServiceAccountKey_appEngineDefault.json'
# Initialize Firebase Admin SDK

cred = credentials.Certificate(service_account_key_path)
initialize_app(cred, {'storageBucket': 'project492-9a253.appspot.com'})

# Initialize Google Cloud Storage client
storage_client = storage.Client()

# Get the bucket reference
bucket = storage_client.get_bucket('project492-9a253.appspot.com')

def upload_images(local_folder, remote_folder):
    for root, dirs, files in os.walk(local_folder):
        for file in files:
            local_file_path = os.path.join(root, file)
            remote_file_path = os.path.join(remote_folder, os.path.relpath(local_file_path, local_folder))

            # Check if the image is already exists in Firebase Cloud Storage
            if not check_image_exists(remote_file_path):
                blob = bucket.blob(remote_file_path)
                blob.upload_from_filename(local_file_path)
                print(f"Uploaded: {local_file_path} to {remote_file_path}")
            else:
                print(f"Skipped: {local_file_path} (Image already exists)")

# Function to check if image already exists in Firebase Cloud Storage
def check_image_exists(remote_file_path):
    try:
        blob = bucket.blob(remote_file_path)
        blob.reload()
        return True
    except storage.exceptions.NotFound:
        return False

# Start the upload process
upload_images(local_images_folder, remote_images_folder)


