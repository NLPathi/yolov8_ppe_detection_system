# 🦺 Real-Time Worker Safety Monitoring Using Deep Learning: A YOLOv8 based Detection System

## 📌 Overview

This project is an **AI-powered worker safety monitoring system** that detects Personal Protective Equipment (PPE) in real-time using two different intelligent approaches:

* 🖼️ **Image Analysis** → Vision Language Model (VLM)
* 🎥 **Video Analysis** → YOLOv8 + OpenCV + SORT Tracking

It ensures accurate PPE compliance detection in industrial and construction environments.

---

## 🚀 Key Features

* 🔍 PPE detection in both images and videos
* 🤖 Vision Language Model for intelligent image understanding
* 🎯 YOLOv8-based real-time object detection
* 👥 Multi-object tracking using SORT algorithm
* 🌐 Web interface using Flask
* ⚡ Fast and scalable safety monitoring system

---

## 🧠 System Approach

### 🖼️ Image Processing (VLM-Based)

* Uses a **Vision Language Model API**
* Converts image to base64 and sends it to the model
* Generates structured JSON output like:

  * Helmet: Yes/No
  * Mask: Yes/No
  * Vest: Yes/No
* Handles partial visibility (e.g., *Head_Not_Visible*)

---

### 🎥 Video Processing (YOLOv8 + SORT)

* Uses **YOLOv8** for object detection
* Uses **OpenCV** for frame processing
* Uses **SORT algorithm** for tracking persons
* Detects:

  * Person
  * Helmet
  * Mask
  * Safety Vest
* Tracks individuals across frames in real-time

---

## 🛠️ Tech Stack

* Python
* YOLOv8 (Ultralytics)
* OpenCV
* Flask
* NumPy
* SORT Tracking Algorithm
* Vision Language Model API

---

## 📂 Project Structure

```id="p9z4ha"
PPE-Detection/
│
├── inference.py              # Main application (image + video logic)
├── sort.py                  # Tracking algorithm
├── classes.txt              # Detection classes
├── names.txt                # PPE labels
├── requirements.txt         # Dependencies
├── PPE.ipynb                # Model training notebook
├── contact_data.json        # Sample data
├── templates/               # HTML files
├── static/                  # CSS/JS files
└── .gitignore
```

---

## ⚙️ Installation

### 1️⃣ Clone Repository

```id="r4z9p0"
git clone https://github.com/NLPathi/yolov8_ppe_detection_system.git
cd yolov8_ppe_detection_system
```

### 2️⃣ Install Dependencies

```id="t7d8qk"
pip install -r requirements.txt
```

---

## 📥 Model & API Setup

### 🔹 YOLO Model

Download `best.pt` from:
👉 **https://drive.google.com/drive/folders/1n0IJCI_VJrgnwcH2bvbkFYiwZ_VHGE4h?usp=drive_link**

Place it in the project directory.

---

### 🔹 Vision API

* Replace API key in `inference.py`

```python id="n3h7vk"
"Authorization": "Bearer YOUR_API_KEY"
```

---

## ▶️ Run the Application

```id="b4z2ls"
python inference.py
```

Open in browser:

```id="f8x1jm"
http://127.0.0.1:5000/
```

---

## 🎯 Use Cases

* Construction site safety monitoring
* Industrial PPE compliance checking
* Smart surveillance systems
* Automated safety auditing

---

## 🔐 Notes

* Model file (`.pt`) is excluded due to size
* Database file is not included for security
* API key must be configured manually

---

## 👨‍💻 Author

**Nakka Lakshmipathi**

---

## ⭐ Future Enhancements

* Real-time alerts (SMS/Email)
* Cloud deployment (AWS/Render)
* Mobile app integration
* Improved detection accuracy

---

## 📢 Conclusion

This project demonstrates a **hybrid AI approach** combining **deep learning (YOLOv8)** and **vision-language models** to build an intelligent and scalable **worker safety monitoring system**.

---
