# 🚀 SurgiTrack Full Backend Architecture Plan

This roadmap outlines the complete backend architecture to make your project scalable, efficient, and deployable.

---

## 📦 1. File Upload and Storage (✔️ IN PROGRESS)

**Tech stack:**

- FastAPI
- AWS S3
- Python `boto3`
- UUID for unique file naming

**Workflow:**

- Accept `.mp4` uploads via `/upload` endpoint
- Validate file type, size (<10MB), and frame rate (<60 FPS)
- Upload to S3 bucket
- Return `file_key` to frontend for further use

---

## 📥 2. File Download and Preprocessing

**Tech stack:**

- S3 client (boto3)
- OpenCV
- Temp file handling via `data/temp_videos/`

**Workflow:**

- Add endpoint like `/process?file_key=...`
- Download the video from S3 to a temp directory
- Pass video path to:
  - `extract_frames.run(video_path)`
  - `detect_frames.run()`
  - `track_object.run()`
- Return `events` (pickup/placed-back) to frontend

---

## 🧠 3. YOLO Object Detection (✔️ DONE)

**Tech stack:**

- YOLOv11 (Ultralytics)
- Trained `.pt` model
- Scripts: `detect_frames.py`, `track_object.py`

**Workflow:**

- Run object detection per frame
- Output bounding boxes in `frame_detections.json`
- Track object events (e.g. "Cup picked up")

---

## 🧠 4. Redis Job Queue (🔄 Optional, but Recommended)

**Tech stack:**

- Redis (via Docker)
- RQ (Redis Queue) or Celery
- `redis-py` or `aioredis`

**Use case:**

- Async handling of long video processing
- Offload jobs to background queue
- Return `job_id` to frontend
- Poll `/status?job_id=...` for updates
- Call `/events?job_id=...` once done

---

## 📂 5. Suggested Project Structure

```
SurgiTrack/
│
├── backend/
│   ├── main.py
│   ├── s3_utils.py
│   ├── redis_queue.py   # optional
│
├── yolo/
│   ├── detect_frames.py
│   ├── extract_frames.py
│   ├── track_object.py
│   ├── __init__.py
│
├── data/
│   ├── temp_videos/
│   ├── frames/
│   └── results/
│
├── uploads/
├── runs/
├── docker-compose.yml
```

---

## 🐳 6. Dockerization (⚙️)

**Tech stack:**

- Docker
- Docker Compose

**Services:**

- `backend` → FastAPI app
- `redis` → Background queue (optional)
- `worker` → Job processor (optional)
- Optional: Nginx reverse proxy

---

## 🌍 7. Frontend Integration (🔁)

**Tech stack:**

- React / Next.js
- `axios` or `fetch`

**Endpoints to connect:**

- `/upload` → Upload .mp4 file
- `/process?file_key=...` → Trigger full processing pipeline
- `/events` → Get final detection event timeline
- Optional: `/status?job_id=...` if using Redis queue

---

## 📊 8. Timeline Visualization (🧠)

**Frontend logic:**

- Use FPS + frame number to convert to timestamps
- Display human-readable timeline:
  ```
  00:04 — Cup picked up
  00:07 — Cup placed back
  ```

---

## 🔐 9. Authentication (Optional for MVP)

**Options:**

- Auth0
- Firebase Auth
- FastAPI JWT-based system

---

## ☁️ 10. Deployment (🚀)

**Options:**

- Fly.io (good for full-stack Docker apps)
- Render.com (easy CI/CD)
- Railway (PostgreSQL + Redis + FastAPI supported)
- AWS EC2 + Nginx + Docker
- Cloudflare Pages (frontend hosting)

---

## 💰 11. Cost & Scaling Notes

**S3 Free Tier:**

- 5 GB standard storage
- 20,000 GET and 2,000 PUT requests monthly (first 12 months)

**Redis:**

- Use local Redis in Docker for dev
- Free tier options on Railway, Fly.io, Upstash

---

## ✅ Final Deliverable Goals

- [ ] Fully working FastAPI backend with endpoints for upload, process, and events
- [ ] Frontend UI for upload + timeline
- [ ] S3 for storage
- [ ] Redis queue (optional)
- [ ] Dockerized for easy deploy
- [ ] Resume-worthy + scalable design
