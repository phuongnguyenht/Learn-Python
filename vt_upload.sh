#!/bin/bash
rm upload_output.txt
export http_proxy=http://192.168.42.8:3128/
export https_proxy=http://192.168.42.8:3128/
swift upload viettalk old_viettalk_images 2>&1 upload_output.txt

