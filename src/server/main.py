from car import Car
import subprocess
from time import sleep
import os

if __name__ == "__main__":
    dir_path = os.path.dirname(__file__)
    # run stream server
    proc_ffserv = subprocess.Popen(['ffserver', '-f ' + dir_path + '/../../camera/ffserver-mjpeg.conf'])
    # wait before run stream process
    sleep(3)
    proc_ff = subprocess.Popen(['ffmpeg', '-f video4linux2 -s 640x480 -r 15 -i /dev/video0 '
                                          'http://localhost:8090/camera.ffm'])

    # run car
    car = Car()

    # kill stream on exit
    proc_ff.kill()
    proc_ffserv.kill()
