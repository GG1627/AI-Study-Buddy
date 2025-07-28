import json

# load the frame detections JSON file with read permission
with open("frame_detections.json", "r") as f:
    data = json.load(f)

# initialize the state of the cup as being on the tray
previous_state = "on_tray"
events = []
    
# loop through each frame in the JSON file
"""
What is happening here?
1. use sorted() to sort the frames by frame number
2. data.keys() uses the key values in the JSON file
3. lambda function sorts the frames by frame number
4. split() splits key value "frame_8" into ["frame", "8"] and uses second element for sorting
"""
for frame_id in sorted(data.keys(), key=lambda x:int(x.split("_")[1])):
    detections = data[frame_id]

    tray = next((d for d in detections if d["label"] == "tray"), None)
    cup = next((d for d in detections if d["label"] == "cup"), None)

    if not tray or not cup:
        continue

    # calculate the center of the cup
    cup_cx = (cup["x1"] + cup["x2"]) / 2
    cup_cy = (cup["y1"] + cup["y2"]) / 2

    if tray["x1"] <= cup_cx <= tray["x2"] and tray["y1"] <= cup_cy <= tray["y2"]:
        current_state = "on_tray"
    else:
        current_state = "off_tray"

    if current_state != previous_state:
        events.append({
            "frame": frame_id,
            "event": "picked up" if current_state == "off_tray" else "placed back"
        })
        previous_state = current_state

for event in events:
    print(f"🕒 {event['frame']}: Cup {event['event']}")







