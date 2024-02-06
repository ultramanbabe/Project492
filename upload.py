import os
import time
import sys
import subprocess
from datetime import datetime
from google.cloud import  storage
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

#Usage nohub python3 upload.py > upload.log 2>&1 &



# Set the name of my Google Cloud Storage Bucket
bucket_name = 'project492-9a253.appspot.com'

# Set Service Account Key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '/home/pi/project492/ServiceAccountKey.json'

# Initialize Google Cloud Storage Client
storage_client = storage.Client()

# Watchdog event handler for monitoring file system changes
class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        elif event.event_type == 'created' or event.event_type == 'modified':

            timestamp = datetime.now().strftime('%d-%m-%Y-%T')

            log_message = f"{timestamp} - Change detected: {event.src_path}"
            upload_image(event.src_path, "images")
            log_to_file(log_message, 'upload.log')

# Function to upload an image to Google Cloud Storage
def upload_image(local_path, cloud_path):
    blob_name = cloud_path + "/" + os.path.relpath(local_path, start='/home/pi/project492/images')

    # Upload image to Google Cloud Storage
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(local_path)

    timestamp = datetime.now().strftime('%d-%m-%Y-%T')

    log_message = f"{timestamp} - Image uploaded Succesfully. Bucket: {bucket_name}, Blob: {blob_name}"
    log_to_file(log_message, 'upload.log')

# Function to perform initial scan and upload existing image
def retroactively_upload(local_path, cloud_path):

    uploaded_files = set() # Set to store uploaded file names to prevent already uploaded file

    for root, dirs, files in os.walk(local_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file not in uploaded_files:
                upload_image(file_path, cloud_path)
                uploaded_files.add(file)

# Function to log messages to a log file
def log_to_file(message, filename):
    with open(filename, 'a') as log_file:
        log_file.write(f'{message}\n')

# Function to start monitoring the images folder
def start_monitoring():
    event_handler = MyHandler()
    observer = Observer()

    # Set the local path on my Raspberry Pi
    local_path = '/home/pi/project492/images'

    # Perform initial scan and upload existing images
    retroactively_upload(local_path, 'images')

    observer.schedule(event_handler, path=local_path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    
  # Run the script in the background using nohup and log output to upload.log 
  #os.system("nohup /home/pi/project492/upload.py > upload.log 2>&1 &")
  #log_file = 'upload.log'
  #subprocess.Popen(["nohup", "python3", "upload.py", ">", "upload.log", "2>&1", "&"])


  # Start monitoring the folder for chages
  start_monitoring()

