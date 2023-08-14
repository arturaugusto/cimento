from flask import Flask, jsonify, render_template, Response, request
import io
import json
import time
import os
import subprocess
from datetime import datetime
try:
  import control_loop
except Exception as e:
  print(e)
  pass



app = Flask(__name__)

@app.route('/api/gravar_pendrive', methods=['POST'])
def gravar_pendrive():
  return
  print("gravar_pendrive")
  data = request.get_json()
  
  res = subprocess.check_output(['ls', '/media/ipt'])
  target_drive = res.decode('utf-8').split('\n')[0]
  print(data)
  # write data...
  now_str = str(datetime.utcnow()).replace('-','_').replace(' ', '').replace(':', '_').replace('.','_')
  
  pen_path = f'/media/ipt/{target_drive}'
  for ch in data.keys():
    with open(f"{pen_path}/{ch}_{now_str}.csv", "w") as f:
      f.write(data[ch])

  umount_res = subprocess.check_output(['umount', pen_path])
  
  
  return jsonify({"target_drive": target_drive})

def event_stream():
  file_size_stored = os.stat('data.txt').st_size
  while True:
    #time.sleep(0.1)
    try:
      file_size_current = os.stat('data.txt').st_size
      if file_size_stored != file_size_current:
        file_size_stored = file_size_current
        with open('data.txt', 'rb') as f:
          try:  # catch OSError in case of a one line file 
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
              f.seek(-2, os.SEEK_CUR)
          except OSError:
            f.seek(0)
          last_line = f.readline().decode()
          print(last_line)
          yield f"data: {last_line}\n\n"
    except: 
      pass


@app.route('/api/stream')
def stream():
  return Response(event_stream(), mimetype="text/event-stream")

@app.route('/api/events', methods=['GET'])
def events():
  with open("data.txt") as file_in:
    lines = []
    for line in file_in:
      lines.append(json.loads(line))
  return jsonify(lines)

@app.route('/')
def root():
  return render_template('/index.html')

if __name__ == '__main__':
  app.run('0.0.0.0', debug=True)
