#! /usr/bin/env bash

# set command vars
CMD='ffserver -f /home/pi/projects/ffcam-stream/ffserver-mjpeg.conf'
CAM0='ffmpeg -f video4linux2 -s 640x480 -r 15 -i /dev/video0 http://localhost:8090/camera.ffm'


# stop old processes before run
`pkill -9 -f "$CAM0"`
`pkill -9 -f "$CMD"`


echo "Killed"
sleep 5


# run
$CMD &
$CAM0 &


echo "Running ..."
sleep 3


ps ax | grep ff