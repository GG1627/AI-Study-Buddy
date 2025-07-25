# 🛠️ SurgiTrack: AI-Powered Tool Usage Tracking System

## 🧩 Overview

**SurgiTrack** is an AI/ML-driven project that detects and tracks the usage of tools (e.g., surgical instruments) from a video feed. By using computer vision and deep learning, the system logs when a tool is picked up, used, and returned — then visualizes this data in a web-based timeline dashboard. Inspired by cleanroom and surgical settings like those at **Arthrex**, this project aims to show real-world applications of AI in medical device environments.

---

## 🎯 Key Features

- Detect and track multiple tools using video analysis
- Log pickup and return timestamps for each tool
- Store and serve tool usage data via an API
- Visualize tool usage on an interactive frontend timeline
- Modular, containerized architecture using Docker

---

## 🧠 Technologies Used

| Component             | Technology                  | Purpose                          |
| --------------------- | --------------------------- | -------------------------------- |
| **Object Detection**  | Ultralytics YOLOv8 + OpenCV | Detect tools in video frames     |
| **Video Processing**  | OpenCV                      | Frame-by-frame analysis          |
| **Backend API**       | FastAPI                     | Serve and log detection events   |
| **Database**          | PostgreSQL or SQLite        | Store tool usage data            |
| **Frontend UI**       | React or Flask + Chart.js   | Visualize timeline of tool usage |
| **Containerization**  | Docker + Docker Compose     | Isolate and deploy services      |
| **ML Infrastructure** | PyTorch                     | Run YOLO model for inference     |

---

## 🧭 Project Architecture

---

## ✅ Step-by-Step Implementation Plan

### 1. 🔍 Project Scoping & Planning

- Define list of tools you want to detect (e.g., scalpel, clamp, scissors)
- Identify a sample video or create one (e.g., surgical tray or cleanroom)
- Decide on initial UI features (timeline chart, tool logs, alerts)

---

### 2. 🎥 Sample Video Collection

- Source a clean, well-lit video where tools are clearly visible
- Focus on top-down or front-facing angles of a tool tray
- Keep it short (~1–2 minutes) to test inference speed and tracking

---

### 3. 🧠 ML/AI Object Detection Setup

- Choose Ultralytics YOLOv8 for pre-trained or fine-tuned object detection
- If needed, label a few frames using Roboflow or CVAT for custom tools
- Test model locally to ensure tools are accurately detected
- Create logic to identify **state changes**:
  - Tool visible → at rest
  - Tool disappears → picked up
  - Tool reappears → returned

---

### 4. 📦 Backend API Development

- Use FastAPI to build endpoints like:
  - `POST /log_event` — save tool usage data
  - `GET /timeline` — return full usage history
  - `GET /tool/{name}` — return history for one tool
- Design a data schema for:
  - Tool name/ID
  - Timestamps of pickup and return
  - Duration used

---

### 5. 🗃️ Database Integration

- Use SQLite for prototyping or PostgreSQL for scaling
- Tables:
  - `tools`: tool metadata
  - `events`: timestamped actions (picked up/returned)
- Ensure timestamps are synced with video frame timestamps

---

### 6. 💻 Frontend Timeline Visualization

- Build UI using:
  - **React + Chart.js or D3.js** _(more dynamic)_
  - or **Flask + Jinja + Plotly** _(easier for full-stack Python)_
- Display timeline:
  - X-axis = time
  - Y-axis = tools
  - Bars = usage duration
- Add filters: date range, tool name, longest usage, etc.

---

### 7. 🐳 Dockerization & DevOps

- Create Docker containers for:
  - `video-processing-service` (YOLOv8 inference)
  - `api-service` (FastAPI backend)
  - `frontend-ui` (React or Flask)
  - `db-service` (PostgreSQL)
- Use Docker Compose to orchestrate everything
- Add `README.md` and `.env` for easy deployment

---

### 8. 🚀 Final Touches & Deployment

- Export logs as CSV for audits or compliance
- Add alert system (e.g., "Tool left out > 10 minutes")
- Optional: deploy to cloud (Render, Railway, or AWS EC2)

---

## 📌 Deliverables for Your Portfolio

- GitHub repo with:
  - Clear README, architecture diagram, and tech summary
  - Screenshots or GIFs of timeline UI
  - Sample video results
- Optional Devpost/Notion page with writeup
- PDF one-pager for recruiters (focused on Arthrex use case)

---

## 🌟 Why This Project Matters (To Arthrex)

- Shows real-world application of AI in surgical environments
- Bridges software engineering + computer vision
- Demonstrates technical depth _and_ awareness of medical manufacturing needs
- Communicates well-rounded engineering skills (ML, full-stack, DevOps)

---
