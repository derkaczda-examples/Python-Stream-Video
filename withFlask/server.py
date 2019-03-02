from flask import Flask, render_template, Response
import sys
import struct
import pickle
import cv2
import socket

app = Flask(__name__)



class VideoCamera(object):
    conn = None
    addr = None

    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        #self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("socket created")
        s.bind(('0.0.0.0', 8089))
        s.listen(10)
        conn, addr = s.accept()
        self.conn = conn
        self.addr = addr

        pass

    def __del__(self):
        #self.video.release()
        pass
    
    def get_frame(self):
        data = ""
        payload_size = struct.calcsize("H")
        while len(data) < payload_size:
            data += self.conn.recv(4069)
        packed_msg_size = data[:payload_size]
        data = data[payload_size]
        msg_size = struct.unpack("H", packed_msg_size)[0]
        while len(data) < msg_size:
            data += self.conn.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        ret, jpeg = cv2.imencode(".jpg", image)

        return jpeg.tobytes()

videoCam = None
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
    return Response(videoCam,
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    videoCam = gen(VideoCamera())
    app.run(host='0.0.0.0', debug=True)
    