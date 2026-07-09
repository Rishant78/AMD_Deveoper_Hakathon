import json
import os
import sys
import requests
from pathlib import Path
from backend.video import get_video_info, extract_frames
from backend.caption import caption_video
from backend.summarizer import summarize_video
from backend.styles import generate_styles


def download_video(video_url, output_path):
    """Download video from URL to local file."""
    print(f"Downloading video from {video_url}...")
    try:
        response = requests.get(video_url, timeout=60)
        response.raise_for_status()
        with open(output_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded to {output_path}")
        return output_path
    except Exception as e:
        print(f"Error downloading video: {e}")
        raise


def process_task(task):
    """Process a single task: download video and generate captions."""
    task_id = task.get('task_id')
    video_url = task.get('video_url')
    requested_styles = task.get('styles', ['formal', 'sarcastic', 'humorous_tech', 'humorous_non_tech'])
    
    print(f"\n--- Processing Task {task_id} ---")
    
    try:
        # Download video
        video_filename = f"task_{task_id}.mp4"
        video_path = os.path.join("uploads", video_filename)
        os.makedirs("uploads", exist_ok=True)
        
        download_video(video_url, video_path)
        
        # Extract frames
        print("Extracting frames...")
        extracted = extract_frames(video_path)
        saved_frames = extracted["saved_frames"]
        
        # Caption each frame
        print("Captioning frames...")
        captioned_frames = caption_video(saved_frames)
        captions = [f["caption"] for f in captioned_frames]
        
        # Generate summary
        print("Generating summary...")
        summary = summarize_video(captions)
        
        # Generate styled captions
        print("Generating styled captions...")
        all_styles = generate_styles(summary)
        
        # Filter to only requested styles
        filtered_styles = {k: v for k, v in all_styles.items() if k in requested_styles}
        
        # Cleanup downloaded video
        os.remove(video_path)
        
        result = {
            "task_id": task_id,
            "captions": filtered_styles
        }
        
        print(f"✓ Task {task_id} completed successfully")
        return result
        
    except Exception as e:
        print(f"✗ Error processing task {task_id}: {e}")
        return {
            "task_id": task_id,
            "error": str(e)
        }


def main():
    """Main batch processor entry point."""
    input_file = "/input/tasks.json"
    output_file = "/output/results.json"
    
    # Ensure output directory exists
    os.makedirs("/output", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)
    
    print("=" * 50)
    print("AMD Captivate AI - Batch Processor")
    print("=" * 50)
    
    # Read input tasks
    if not os.path.exists(input_file):
        print(f"Error: Input file not found at {input_file}")
        sys.exit(1)
    
    try:
        with open(input_file, 'r') as f:
            tasks = json.load(f)
    except Exception as e:
        print(f"Error reading input file: {e}")
        sys.exit(1)
    
    if not isinstance(tasks, list):
        print("Error: Input must be a JSON array of tasks")
        sys.exit(1)
    
    print(f"Found {len(tasks)} task(s) to process")
    
    # Process each task
    results = []
    for task in tasks:
        result = process_task(task)
        results.append(result)
    
    # Write results
    try:
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n✓ Results written to {output_file}")
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("Batch processing complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()
