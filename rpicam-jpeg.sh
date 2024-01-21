#!/bin/bash

#rpicam-jpeg --width 2592 --height 1944 -q 100 -o test.jpg

rpicam-jpeg --width 2592 --height 1944 -q 100 -t 5000 --shutter 200000 --gain 2 -n  -o test.jpg
