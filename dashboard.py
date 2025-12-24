import os
import shutil
from flask import Flask, request, render_template_string, redirect, url_for
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

detection_logs = []

@app.route('/')
def index():
    html_template = '''
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <title>Dashboard Monitoring</title>
        <meta http-equiv="refresh" content="2"> 
        <style>
            body { font-family: 'Segoe UI', sans-serif; margin: 0; background-color: #f4f4f9; }
            
            .header { 
                background-color: #007bff; 
                padding: 15px 30px; 
                display: flex; 
                justify-content: flex-end; 
                align-items: center; 
                height: 50px; 
            }
            
            .container { padding: 30px; max-width: 1200px; margin: 0 auto; }
            table { width: 100%; border-collapse: collapse; background: white; }
            th, td { text-align: left; padding: 15px; border-bottom: 1px solid #eee; }
            th { background-color: #343a40; color: white; }
            
            .btn-reset {
                background-color: #dc3545; 
                color: white; 
                border: 2px solid #b21f2d; 
                padding: 8px 20px; 
                border-radius: 4px; 
                cursor: pointer; 
                font-weight: bold; 
                font-size: 14px;
                text-transform: uppercase;
            }
            .btn-reset:hover { background-color: #c82333; }
        </style>
    </head>
    <body>
        <div class="header">
            <form action="/clear" method="post" onsubmit="return confirm('Hapus semua data?');">
                <button type="submit" class="btn-reset">RESET DATA</button>
            </form>
        </div>

        <div class="container">
            <table>
                <thead>
                    <tr>
                        <th>Jam</th>
                        <th>Foto</th>
                        <th>ID</th>
                        <th>Jenis</th>
                        <th>Jumlah</th>
                    </tr>
                </thead>
                <tbody>
                    {% for log in logs|reverse %}
                    <tr>
                        <td>{{ log.timestamp }}</td>
                        <td>
                            {% if log.image_path %}
                            <a href="{{ log.image_path }}" target="_blank">
                                <img src="{{ log.image_path }}" height="50">
                            </a>
                            {% else %}-{% endif %}
                        </td>
                        <td>#{{ log.track_id }}</td>
                        <td>{{ log.class_name }}</td>
                        <td><b>{{ log.count }}</b></td>
                    </tr>
                    {% else %}
                    <tr>
                        <td colspan="5" style="text-align:center; padding: 50px; color: gray;">
                            <i>Data kosong. Sistem siap menerima data.</i>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html_template, logs=detection_logs)

@app.route('/api/upload', methods=['POST'])
def upload_data():
    if 'image' not in request.files: return "No image", 400
    file = request.files['image']
    track_id = request.form.get('track_id')
    class_name = request.form.get('class_name')
    count = request.form.get('count')
    
    timestamp_str = datetime.now().strftime("%H:%M:%S")
    filename = f"{timestamp_str.replace(':','-')}_{track_id}.jpg"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    
    detection_logs.append({
        'timestamp': timestamp_str, 'image_path': filepath,
        'track_id': track_id, 'class_name': class_name, 'count': count
    })
    return "OK", 200

@app.route('/clear', methods=['POST'])
def clear_data():
    global detection_logs
    detection_logs = []
    try:
        for f in os.listdir(UPLOAD_FOLDER):
            os.remove(os.path.join(UPLOAD_FOLDER, f))
    except: pass
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)