import os
from flask import Flask, send_from_directory

app = Flask(__name__)

# Static files aur index.html serve karne ke liye route
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Agar folder mein aur koi files hain unhe serve karne ke liye
@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    # Render ya local host dono par chalne ke liye port configuration
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)