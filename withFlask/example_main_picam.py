##
## example from  http://www.chioka.in/python-live-video-streaming-example/
##

from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2


class VideoCamera(object):
    def __init__(self):
	global camera
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = PiCamera() #cv2.VideoCapture(0)
	self.video.resolution = (640,480)
	self.video.framerate = 32
        self.rawCapture = PiRGBArray(self.video, size=(640,480))
	# If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    
    def __del__(self):
        #self.video.release()
	self.video.close()
    	pass
    def get_frame(self):
        #success, image = self.video.read()
        self.video.capture(self.rawCapture, format="bgr")
	image = self.rawCapture.array
	# We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
	self.rawCapture.truncate(0)
        return jpeg.tobytes()

from flask import Flask, render_template, Response
#from camera import VideoCamera

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
#camera = PiCamera()
if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=True)
