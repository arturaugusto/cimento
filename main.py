from flask import Flask, jsonify, render_template, Response, request
import io
import json
import time
import os
try:
  import control_loop
except Exception as e:
  print(e)
  pass



app = Flask(__name__)

def event_stream():
  file_size_stored = os.stat('data.txt').st_size
  while True:
    time.sleep(0.1)
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
  app.run('0.0.0.0', debug=False)
