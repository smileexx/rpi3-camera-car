#! /usr/bin/env bash

CMD='ffserver -f /home/pi/projects/ffcam-stream/ffserver-mjpeg.conf'
CAM0='ffmpeg -f video4linux2 -s 640x480 -r 15 -i /dev/video0 http://localhost:8090/camera.ffm'

# Stop process by name
`pkill -9 -f "$CAM0"`
`pkill -9 -f "$CMD"`

# delay for killing
sleep 3

echo "All stopped"

# show that we don't have ffmpeg process anymore
ps ax | grep ff