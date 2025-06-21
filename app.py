from flask import Flask, request, jsonify
import subprocess
import uuid
import os
import requests

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data.get("prompt", "")
    output_name = f"{uuid.uuid4().hex}.png"
    command = [
        "python3", "pixray/pixray.py",
        f"prompt={prompt}",
        "drawer=pixel",
        "display=False",
        f"output={output_name}"
    ]
    subprocess.run(command)
    return jsonify({"image": output_name})


# ⬇️ ADD THIS NEW RENDER ROUTE BELOW
@app.route('/render', methods=['POST'])
def render_video():
    data = request.get_json()

    image_url = data.get("image")
    audio_url = data.get("audio")
    subtitles_url = data.get("subtitles")
    output_name = f"{uuid.uuid4().hex}.mp4"

    image_file = "input.jpg"
    audio_file = "audio.mp3"
    subtitles_file = "subs.srt"

    def download_file(url, path):
        r = requests.get(url)
        r.raise_for_status()
        with open(path, "wb") as f:
            f.write(r.content)

    try:
        download_file(image_url, image_file)
        download_file(audio_url, audio_file)
        download_file(subtitles_url, subtitles_file)
    except Exception as e:
        return jsonify({"error": f"Download failed: {str(e)}"}), 400

    command = [
        "ffmpeg",
        "-y",
        "-loop", "1",
        "-i", image_file,
        "-i", audio_file,
        "-vf", f"subtitles={subtitles_file}",
        "-shortest",
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        output_name
    ]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"FFmpeg failed: {str(e)}"}), 500

    return jsonify({"video": output_name})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
