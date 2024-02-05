import os
import time
import sys
from google.cloud import  storage
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

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
            log_message = f"Change detected: {event.src_path}"
            upload_image(event.src_path, "images")
            log_to_file(log_message, 'upload_log.log')

# Function to upload an image to Google Cloud Storage
def upload_image(local_path, cloud_path):
    blob_name = cloud_path + "/" + os.path.relpath(local_path, start='/home/pi/project492/images')

    # Upload image to Google Cloud Storage
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(local_path)

    log_message = f"Image uploaded Succesfully. Bucket: {bucket_name}, Blob: {blob_name}"
    log_to_file(log_message, 'upload_log.log')

# Function to perform initial scan and upload existing image
def retroactively_upload(local_path, cloud_path):
    for root, dirs, files in os.walk(local_path):
        for file in files:
            file_path = os.path.join(root, file)
            upload_image(file_path, cloud_path)

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

if __name__ == "__main__":
    
    
    # Run the script in the background using nohup
    os.system("nohup python3 upload.py &")

    try:
        # Start monitoring the folder for changes
        start_monitoring()
    except KeyboardInterrupt:
        # Handle keyboard interrupt to stop the script and terminate the background process
        os.system("pkill -f 'python3 upload.py'")
