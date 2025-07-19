import json
import os

def normalize_glyph(input_file, output_file=None, target_height=30):
    """
    Normalize a glyph JSON file by:
    1. Finding the bounding box
    2. Shifting to start at (0,0)
    3. Scaling to target height
    4. Preserving original structure
    """
    
    # Load the JSON file
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    strokes = data["strokes"]
    
    # Find bounding box
    all_x = [pt["x"] for stroke in strokes for pt in stroke["points"]]
    all_y = [pt["y"] for stroke in strokes for pt in stroke["points"]]
    min_x, min_y = min(all_x), min(all_y)
    max_x, max_y = max(all_x), max(all_y)
    
    print(f"Original bounds: ({min_x}, {min_y}) to ({max_x}, {max_y})")
    print(f"Original size: {max_x - min_x} x {max_y - min_y}")
    
    # Scale to target height
    scale = target_height / (max_y - min_y)
    
    # Create normalized strokes with original structure
    normalized_strokes = []
    for stroke in strokes:
        normalized_points = []
        for pt in stroke["points"]:
            normalized_points.append({
                "x": int((pt["x"] - min_x) * scale),
                "y": int((pt["y"] - min_y) * scale),
                "time": pt["time"],
                "pressure": pt["pressure"]
            })
        
        # Preserve original stroke structure
        normalized_stroke = {
            "points": normalized_points,
            "startTime": stroke["startTime"],
            "endTime": stroke["endTime"]
        }
        normalized_strokes.append(normalized_stroke)
    
    # Create output data with metadata
    output_data = {
        "metadata": {
            "captureDate": data["metadata"]["captureDate"],
            "canvasWidth": int((max_x - min_x) * scale),
            "canvasHeight": target_height,
            "totalStrokes": len(normalized_strokes),
            "totalPoints": sum(len(stroke["points"]) for stroke in normalized_strokes),
            "device": data["metadata"]["device"],
            "original_bounds": {"min_x": min_x, "min_y": min_y, "max_x": max_x, "max_y": max_y},
            "normalized_height": target_height,
            "scale_factor": scale
        },
        "strokes": normalized_strokes
    }
    
    # Save to output file
    if output_file is None:
        base_name = os.path.splitext(input_file)[0]
        output_file = f"{base_name}_normalized.json"
    
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"Normalized bounds: (0, 0) to ({int((max_x - min_x) * scale)}, {target_height})")
    print(f"Saved to: {output_file}")
    
    return output_data

if __name__ == "__main__":
    # Normalize just the H.json file
    print("Normalizing H.json...")
    normalize_glyph("characters/H.json", target_height=30)