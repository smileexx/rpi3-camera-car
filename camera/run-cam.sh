#! /usr/bin/env bash

CMD='ffserver -f /home/pi/projects/ffcam-stream/ffserver-mjpeg.conf'
CAM0='ffmpeg -f video4linux2 -s 640x480 -r 15 -i /dev/video0 http://localhost:8090/camera1.ffm'
CAM1='ffmpeg -f video4linux2 -s 640x480 -r 15 -i /dev/video1 http://localhost:8090/camera.ffm'


`pkill -9 -f "$CAM0"`
`pkill -9 -f "$CAM1"`
`pkill -9 -f "$CMD"`

echo "Killed"

sleep 5

$CMD &
$CAM0 &
$CAM1 &

echo "Running ..."

sleep 3

ps ax | grep ff