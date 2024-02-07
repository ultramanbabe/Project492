import os
import firebase_admin
from firebase_admin import credentials, storage
from datetime import datetime

# Set Service Account Key
os.environ["GOOGLE_APPLICATOIN_CREDENTIALS"] = '/home/pi/project492/ServiceAccountKey.json'
cred = credentials.Certificate('/home/pi/project492/ServiceAccountKey.json')
# Initialize Firebase
firebase_admin.initialize_app(cred, {'storageBucket': 'project492-9a253.appspot.com'})

bucket = storage.bucket()

def list_files_in_local_folder(local_folder):
    file_list = []
    for root, dirs, files in os.walk(local_folder):
        for file in files:
            file_path = os.path.join(root, file)
            file_list.append({
                'path': file_path,
                'modified_time': os.path.getmtime(file_path)
                })
    return file_list

def list_files_in_firebase_storage():
    blobs = bucket.list_blobs()
    return [{'path': blob.name, 'modified_time': blob.time_created.timestamp()} for blob in blobs]

def sync_files(local_files, cloud_files):
    for local_file in local_files:
        cloud_file = next((file for file in cloud_files if file['path'] == local_file['path']), None)
        if not cloud_file or local_file['modified_time'] > cloud_file['modified_time']:
            upload_file_to_firebase(local_file['path'])

def upload_file_to_firebase(file_path):
    blob = bucket.blob(file_path[len(local_folder):].lstrip('/')) # Removes the base folder path
    blob.upload_from_filename(file_path)
    print(f'Uploaded {file_path} to Firebase Storage.')

if __name__ == '__main__':
    local_folder = '/home/pi/project492/images/'
    local_files = list_files_in_local_folder(local_folder)
    cloud_files = list_files_in_firebase_storage()
    sync_files(local_files, cloud_files)
