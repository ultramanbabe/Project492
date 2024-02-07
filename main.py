#!/usr/bin/python3

import subprocess
import os
from datetime import datetime

#create folder each day
#parent folder
images_folder = "/home/pi/project492/images"
#subfolder
current_date = datetime.now().strftime("%d-%m-%Y")
subfolder_name = current_date
subfolder_path = os.path.join(images_folder, subfolder_name)

#check if the folder exists
if not os.path.exists(subfolder_path):
    #create subfolder
    os.mkdir(subfolder_path)
    print(f"Subfolder '{subfolder_name}' created succesfilly in '{images_folder}'.")
else:
    print(f"Subfolder '{subfolder_name}' already exist in '{images_folder}'.")

#capture image
subprocess.run('rpicam-jpeg --width 2592 --height 1944 -q 100 -t 3000 --shutter 200000 --gain 1.5 --verbose 0 -n -o /home/pi/project492/images/"$(date "+%d-%m-%Y")"/"$(date +%d-%m-%Y-%T)".jpg' , shell=True)


