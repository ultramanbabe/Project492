import os
import firebase_admin
import time
from firebase_admin import credentials, storage
from datetime import datetime

# Initialize Firebase
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '/home/pi/project492/ServiceAccountKey.json'
cred = credentials.Certificate('/home/pi/project492/ServiceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'project492-9a253.appspot.com'
    })
bucket = storage.bucket()

# Reading files as a list
def list_files_in_local_folder(local_folder):
    file_list = []
    for root, dirs, files in os.walk(local_folder):
        for file in files:
            file_path = os.path.join(root, file)
            cloud_path = os.path.join('images', os.path.relpath(file_path, local_folder))
            file_list.append({'local_path': file_path, 'cloud_path': cloud_path})
    return file_list

# Reading folder as a list
def list_folders_in_local_folder(local_folder):
    folder_list = []
    for dir in dirs: 
        folder_path = os.path.join(root, dir)
        cloud_path = os.path.join('images', os.path.relpath(folder_path, local_folder))
        folder_list.append({'local_path': folder_path, 'cloud_path': cloud_path})
    return folder_list

def list_files_in_firebase_storage():
    blobs = bucket.list_blobs()
    return {blob.name: blob.time_created.timestamp() for blob in blobs}

def sync_files(local_files, cloud_files):
    for local_file in local_files:
        cloud_modification_time = cloud_files.get(local_file['cloud_path'])
        if not cloud_modification_time or os.path.getmtime(local_file['local_path']) > cloud_modification_time:
            upload_file_to_firebase(local_file['local_path'], local_file['cloud_path'])

    # Check for deletions
    for cloud_path, cloud_modification_time in cloud_files.items():
        local_path = os.path.join(local_folder, os.path.relpath(cloud_path, 'images'))
        if not os.path.exists(local_path):
            delete_file_from_firebase(local_path, cloud_path)

def upload_file_to_firebase(local_path, cloud_path):
    blob = bucket.blob(cloud_path)
    blob.upload_from_filename(local_path)
    print(f'Uploaded {local_path} to Firebase under {cloud_path}.')

def delete_file_from_firebase(local_path, cloud_path):
    blob = bucket.blob(cloud_path)
    blob.delete()
    print(f'Deleted {local_path} from Firebase.')



if __name__ == '__main__':
    time.sleep(10) 
    local_folder = '/home/pi/project492/images'
    local_files = list_files_in_local_folder(local_folder)
    cloud_files = list_files_in_firebase_storage()
    sync_files(local_files, cloud_files)
