import re
import json
from flask import Flask, render_template, request, jsonify, redirect, url_for,session,Response,Request
from flask_cors import CORS
import cv2
from flask_wtf.csrf import CSRFProtect
import numpy as np
from ultralytics import YOLO
import cvzone
import sqlite3
from sort import *
import ast
import requests, base64
import threading

app = Flask(__name__)
CORS(app)

# Set a secret key for sessions
app.config['SECRET_KEY'] = 'a' 

# Path to store the JSON file
JSON_FILE = "contact_data.json"

invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"

stream = False

@app.route("/", methods=["GET", "POST"])
def project():
    return render_template("index.html")

@app.route("/hero")
def home():
    return render_template("index.html")

@app.route("/model")
def model():
    return render_template("model.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        conn = sqlite3.connect('projectDatabase.db')
        c = conn.cursor()

        c.execute("DROP TABLE IF EXISTS userDetails")

        c.execute('''CREATE TABLE IF NOT EXISTS userDetails(
                    firstName TEXT,
                    lastName TEXT,
                    email TEXT UNIQUE,
                    password TEXT)''')

        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        password = request.form.get("password")

        try:
            c.execute("INSERT INTO userDetails (firstName, lastName, email, password) VALUES (?, ?, ?, ?)",
                      (firstname, lastname, email, password))
            conn.commit()
            message = "Registration successful!"
            status = "success"
        except sqlite3.IntegrityError:
            message = "Email already exists!"
            status = "error"
        
        conn.close()
        return render_template("login.html", message=message, status=status)
    else:
        return render_template("register.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/submit_contact", methods=["POST"])
def submit_contact():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    contact_entry = {"name": name, "email": email, "message": message}

    try:
        with open(JSON_FILE, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []

    data.append(contact_entry)

    with open(JSON_FILE, "w") as file:
        json.dump(data, file, indent=4)

    return jsonify({"status": "success", "message": "Contact details saved!"}), 200

@app.route("/login", methods=["POST"])
def log_in():
    conn = sqlite3.connect('projectDatabase.db')
    c = conn.cursor()

    firstname = request.form.get('firstname')  
    password = request.form.get('password')

    c.execute("SELECT EXISTS(SELECT 1 FROM userDetails WHERE firstname=? AND password=?)", (firstname, password))
    flag = c.fetchone()[0]

    conn.commit()
    conn.close()

    if flag == 1:
        session['user'] = firstname
        return render_template("model.html")
    else:
        return render_template('login.html', error="Invalid credentials, please try again.")

# Allowed extensions
IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "bmp"}
VIDEO_EXTENSIONS = {"mp4", "avi", "mov", "mkv"}

def allowed_file(filename, allowed_extensions):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions

outputFrame = None
lock = threading.Lock()

@app.route("/")
def video_feed_template():
    return render_template("video_feed.html")

@app.route("/predict", methods=["POST","GET"])
def predict():
    global outputFrame

    if "file" not in request.files:
        return jsonify({"error": "File is required"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = file.filename.lower()
    print(filename)

    if file and allowed_file(filename, IMAGE_EXTENSIONS):
        image_path = os.path.join("ppe_image", filename)
        file.save(image_path)

        with open(f"{image_path}", "rb") as f:
            image_b64 = base64.b64encode(f.read()).decode()
            
            headers = {
            "Authorization": "Bearer YOUR_API_KEY",
            "Accept": "application/json"
            }

            prompt = "Analyse the image and return PPE JSON"

            payload = {
            "model": 'microsoft/phi-3.5-vision-instruct',
            "messages": [
                {
                "role": "user",
                "content": f'{prompt}  <img src="data:image/jpeg;base64,{image_b64}" />'
                }
            ]
            }

            response = requests.post(invoke_url, headers=headers, json=payload)
           

            data = response.json()

            if "choices" in data:
                content = data["choices"][0]["message"]["content"]

                try:
                    if content.startswith("```json"):
                        content = content.strip("```json").strip("```")

                    ppe_data = json.loads(content)
                    return jsonify({'predictions': ppe_data})

                except:
                    return jsonify({"error": "JSON parse error"})

    elif file and allowed_file(filename, VIDEO_EXTENSIONS):
        video_path = os.path.join("ppe_video", filename)
        file.save(video_path)

        cap = cv2.VideoCapture(video_path)
        tracker = Sort(max_age=30)

        classnames = []
        with open('classes.txt', 'r') as f:
            classnames = f.read().splitlines()

        model = YOLO('best.pt')

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            detections = np.empty((0, 5))
            results = model(frame)

            for info in results:
                boxes = info.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    conf = box.conf[0]
                    classindex = box.cls[0].item()
                    object_detected = classnames[int(classindex)]

                    if object_detected and conf > 0.1:
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                        new_detections = np.array([x1, y1, x2, y2, conf])

                        if object_detected == "Person":
                            detections = np.vstack((detections, new_detections))
                        else:
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                            cvzone.putTextRect(frame, f'{object_detected}', [x1 + 5, y1 - 10])

            track_result = tracker.update(detections)

            for result in track_result:
                x1, y1, x2, y2, obj_id = map(int, result)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cvzone.putTextRect(frame, f'Person {obj_id}', [x1 + 5, y1 - 10])

            with lock:
                outputFrame = frame.copy()

        return jsonify({"data":True, "video_path": video_path}), 200

    else:
        return jsonify({"error": "Invalid file type"}), 400


def generate():
    global outputFrame, lock

    while True:
        with lock:
            if outputFrame is None:
                continue

            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

            if not flag:
                continue

        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' +
              bytearray(encodedImage) + b'\r\n')

@app.route("/video_feed")
def video_feed():
    return Response(generate(),
        mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    app.run(debug=True)