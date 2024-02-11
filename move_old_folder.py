#!/usr/bin/python3

import os
import shutil
from datetime import datetime, timedelta

def move_old_folder(source_folder, destination_folder, threshold_days): # Move folder older than threshold_days from source_folder to destination_folder

    # Get current time
    current_time = datetime.now()
    # Calculate the threshold date
    threshold_date = current_time - timedelta(days=threshold_days)

    # Iterate over folders in the source folder
    for folder_name in os.listdir(source_folder):
        folder_path = os.path.join(source_folder, folder_name)
        # Check if it's a folder
        if os.path.isdir(folder_path):
            # Get the last modified time of the folder
            modified_time = datetime.fromtimestamp(os.path.getmtime(folder_path))
            # If the folder is older than the threshold, move it
            if modified_time < threshold_date:
                destination_path = os.path.join(destination_folder, folder_name)
                shutil.move(folder_path, destination_path)
                print(f'Moved {folder_path} to {destination_path}')

if __name__ == "__main__":
    source_folder = '/home/pi/project492/images'
    destination_folder = '/home/pi/project492/old_images'
    threshold_days = 2
    move_old_folder(source_folder, destination_folder, threshold_days)

