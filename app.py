import os
import subprocess
import uuid
from flask import Flask, request, jsonify

app = Flask(__name__)

# Tentukan path ke file main lua Prometheus
# Sesuaikan 'Prometheus/main.lua' dengan lokasi file asli kamu
PROMETHEUS_SCRIPT = "Prometheus/src/main.lua" 
# Note: Cek struktur folder kamu, kadang ada di dalam folder 'src'

@app.route('/', methods=['GET'])
def home():
    return "Prometheus API is Running!"

@app.route('/obfuscate', methods=['POST'])
def obfuscate():
    data = request.json
    script_content = data.get('script')

    if not script_content:
        return jsonify({"error": "No script provided"}), 400

    # Buat nama file unik agar tidak bentrok antar user
    unique_id = str(uuid.uuid4())
    input_filename = f"temp_{unique_id}.lua"
    
    # Tulis script user ke file sementara
    with open(input_filename, "w") as f:
        f.write(script_content)

    try:
        # Jalankan perintah: lua5.1 main.lua --script input.lua
        # Sesuaikan argumen command line sesuai dokumentasi Prometheus
        cmd = ["lua5.1", PROMETHEUS_SCRIPT, "--script", input_filename]
        
        # Jalankan process
        process = subprocess.run(cmd, capture_output=True, text=True)

        if process.returncode != 0:
            return jsonify({"error": "Obfuscation failed", "details": process.stderr}), 500

        # Prometheus biasanya print hasil ke console (stdout) atau ke file.
        # Jika output ke console:
        obfuscated_code = process.stdout

        # Bersihkan file sementara
        if os.path.exists(input_filename):
            os.remove(input_filename)

        return jsonify({
            "status": "success",
            "obfuscated_code": obfuscated_code
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)