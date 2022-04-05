import cv2
import numpy as np
from flask import Flask,request,make_response,jsonify

app=Flask(__name__)

@app.route("/edge",methods=["POST"])
def detect_edge():
    fl=20
    sl=30
    if "image" not in request.files:
        return jsonify({"error":"image not provided"})
    file=request.files["image"]
    img=cv2.imdecode(np.frombuffer(file.stream.read(),np.uint8),-1)
    img_greyscale=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img_gs_blur=cv2.GaussianBlur(img_greyscale,(7,7),0)
    img_canny=cv2.Canny(img_gs_blur,fl,sl)
    retval,buffer=cv2.imencode(".png",img_canny)
    response=make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/png'
    return response

if __name__=="__main__":
    app.run("0.0.0.0",8080)