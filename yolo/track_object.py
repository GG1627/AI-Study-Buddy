import json
import datetime
from pathlib import Path

def run():
     # Use absolute path
    project_root = Path(__file__).parent.parent
    json_path = project_root / "yolo" / "frame_detections.json"

     # Check if detections file exists
    if not json_path.exists():
        raise Exception(f"❌ Detections file not found: {json_path}")
        
    # example FPS
    FPS = 30

    # load the frame detections JSON file with read permission
    with open(str(json_path), "r") as f:
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
        # get the values of each key from the JSON file
        detections = data[frame_id]

        # get the "cup" and "tray" detections only if they exist
        tray = next((d for d in detections if d["label"] == "tray"), None)
        cup = next((d for d in detections if d["label"] == "cup"), None)

        # if no tray or cup is detected, skip the frame - probably a mistake
        if not tray or not cup:
            continue

        # calculate the center of the cup
        cup_cx = (cup["x1"] + cup["x2"]) / 2
        cup_cy = (cup["y1"] + cup["y2"]) / 2

        # check if the cup is on the tray
        if tray["x1"] <= cup_cx <= tray["x2"] and tray["y1"] <= cup_cy <= tray["y2"]:
            current_state = "on_tray"
        else:
            current_state = "off_tray"

        # if the cup is picked up or placed back, add an event
        if current_state != previous_state:

            # calculate the time in seconds since the first frame
            frame_num = int(frame_id.split("_")[1])
            time_sec = frame_num / FPS
            timestamp = str(datetime.timedelta(seconds=time_sec))

            events.append({
                "frame": frame_id,
                "timestamp": timestamp,
                "event": "picked up" if current_state == "off_tray" else "placed back"
            })
            previous_state = current_state

    return events







