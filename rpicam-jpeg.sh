#!/bin/bash

#rpicam-jpeg --width 2592 --height 1944 -q 100 -o test.jpg

#rpicam-jpeg --width 2592 --height 1944 -q 100 -t 3000 --shutter 300000 --gain 1.5 -n  -o test.jpg

rpicam-jpeg --width 2592 --height 1944 -q 100 -t 3000 --shutter 200000 --gain 1.5 -n -o ./images/"$(date +%F-%T)".jpg

