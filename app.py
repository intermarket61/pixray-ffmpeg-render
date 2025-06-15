from flask import Flask, request, jsonify
import subprocess
import uuid

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)