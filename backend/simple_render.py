import json, cv2, numpy as np
from moviepy.editor import ImageSequenceClip

# 1. Load your captured JSON
data = json.load(open("./characters/H_normalized.json"))
strokes = data["strokes"]

# 2. Settings
W, H = 800, 400
fps = 24
frames_per_stroke = 15

# 3. Draw frames
frames = []
for stroke_idx, stroke in enumerate(strokes):
    pts = [(p["x"], p["y"]) for p in stroke["points"]]
    for t in np.linspace(1, len(pts), frames_per_stroke, dtype=int):
        canvas = np.zeros((H, W, 3), dtype=np.uint8)  # black BG
        
        # Draw all completed strokes first
        for i in range(stroke_idx):
            s = strokes[i]
            pts2 = [(p["x"], p["y"]) for p in s["points"]]
            if len(pts2) > 1:
                for j in range(len(pts2)-1):
                    cv2.line(canvas, pts2[j], pts2[j+1], (200,200,200), 4, lineType=cv2.LINE_AA)
        
        # Draw current stroke partially
        pts2 = pts[:t]
        if len(pts2) > 1:
            for i in range(len(pts2)-1):
                cv2.line(canvas, pts2[i], pts2[i+1], (200,200,200), 4, lineType=cv2.LINE_AA)
        
        frames.append(canvas)

# 4. Turn frames into a clip and save
clip = ImageSequenceClip([cv2.cvtColor(f, cv2.COLOR_BGR2RGB) for f in frames], fps=fps)
clip.write_videofile("demo_H.mp4", codec="libx264")