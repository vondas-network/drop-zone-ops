from obswebsocket import obsws, requests, exceptions
import os
import sys
import time


import threading
import logging
import json
from flask import Flask, request, jsonify, render_template, redirect, url_for, send_from_directory
import m3u8
from datetime import datetime, timedelta
import obsws_python as obs

# Configure logging
logging.basicConfig(filename='obs_stream.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

app = Flask(__name__)

# Define connection parameters
host = 'localhost'
wsport = 4455
password = 'password'



@app.route('/css/<path:path>')
def send_report(path):
    return send_from_directory('static', path)










##########
# scheduler
###########

schedule_file = 'schedule.json'


# Global variables to control the streaming
stream_active = False
current_playlist = ""
schedule = []
stop_streaming = threading.Event()
stream_schedule = {}  # To store multiple scheduled start/stop times

def parse_playlist(playlist_path):
    try:
        if playlist_path.startswith('http://') or playlist_path.startswith('https://'):
            playlist = m3u8.load(playlist_path)
        else:
            with open(playlist_path, 'r') as f:
                playlist = m3u8.load(f)
        videos = []
        run_time = 0
        for segment in playlist.segments:
            videos.append({'title': '.'.join(segment.title.split('.')[:-1]), 'start_time': run_time})
            run_time += segment.duration
        return videos
    except Exception as e:
        logging.error(f"Error loading playlist: {e}")
        return []


def start_stream(playlist_path, stream_name):
    global stream_active, current_playlist, schedule
    try:
        # Initialize the OBS WebSocket client using ReqClient (connects automatically)
        cl = obs.ReqClient(host=host, port=wsport, password=password, timeout=3)

        # get base_width and base_height
        video_settings = cl.get_video_settings()
        base_width = video_settings.base_width
        base_height = video_settings.base_height

        scene_name = stream_name  # Name of the scene in OBS

        # get existing scenes
        raw_list = cl.get_scene_list()
        scene_list = [a['sceneName'] for a in raw_list.scenes]

        # if doesnt already exist create scene with this name
        if scene_name not in scene_list:
            cl.create_scene(scene_name)
        cl.set_current_program_scene(scene_name)

        input_name = scene_name + " - vlc playlist"  # Name for the media source in OBS

        raw_list = cl.get_scene_item_list(scene_name)
        scene_item_list = [a['sourceName'] for a in raw_list.scene_items]

        # if source doesnt already exist create source with this name
        if input_name not in scene_item_list:
            full_playlist_path = playlist_path
            input_kind = "vlc_source"  # Kind of input (VLC source)
            input_settings = {
                "playlist": [{"hidden": False,"selected": False,"value": full_playlist_path}]
            }
            scene_item_enabled = True  # Set to True to enable the scene item
            # Create the VLC media source input
            settings = cl.create_input(scene_name, input_name, input_kind, input_settings, scene_item_enabled)

        # transform -> fit to screen
        scene_item_id = cl.get_scene_item_id(scene_name, input_name, offset=None).scene_item_id
        cl.set_scene_item_transform(scene_name, scene_item_id, {'boundsWidth': base_width, 'boundsHeight': base_height, 'boundsType': 'OBS_BOUNDS_SCALE_INNER'})

        # ----------------------------
        # Start the stream
        # logging.info("Starting stream with playlist: {}".format(playlist_path))
        # current_playlist = playlist_path
        # start_time = datetime.now()
        # cl.start_stream()
        # stream_active = True

    except Exception as e:
        logging.error(f"OBS Error: {e}")
    finally:
        cl.disconnect()

def stop_stream():
    global stream_active
    try:
        # Initialize the OBS WebSocket client using ReqClient (connects automatically)
        cl = obs.ReqClient(host=host, port=wsport, password=password, timeout=3)

        # Stop the stream
        logging.info("Stopping stream")
        cl.stop_stream()
        stream_active = False

    except Exception as e:
        logging.error(f"OBS Error: {e}")
    finally:
        cl.disconnect()

def scheduled_stream():
    while not stop_streaming.is_set():
        current_time = datetime.now()
        for key, times in stream_schedule.items():
            start_time = datetime.strptime(times['start_time'], '%Y-%m-%dT%H:%M')
            stop_time = datetime.strptime(times['stop_time'], '%Y-%m-%dT%H:%M')
            playlist_path = times['playlist']
            stream_name = times['stream_name']

            if start_time <= current_time < stop_time and not stream_active:
                start_stream(playlist_path, stream_name)
            elif current_time >= stop_time and stream_active:
                stop_stream()
        time.sleep(60)  # Check every minute

def load_schedule():
    global schedule
    if os.path.exists(schedule_file):
        with open(schedule_file, 'r') as f:
            schedule = json.load(f)

def save_schedule():
    with open(schedule_file, 'w') as f:
        json.dump(schedule, f, indent=4)

def get_obs_state():
    obs_state = {
        'obs_running': False,
        'streaming': False,
        'recording': False
    }
    try:
        cl = obs.ReqClient(host=host, port=wsport, password=password, timeout=3)
        obs_state.update({
            'obs_running': True,
            'streaming': cl.get_stream_status().output_active,
            'recording': cl.get_record_status().output_active
        })
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    return obs_state

@app.route('/')
def index():
    load_schedule()
    obs_state = get_obs_state()
    return render_template('index.html', current_playlist=current_playlist, schedule=schedule, obs_state=obs_state)

@app.route('/schedule', methods=['POST'])
def schedule_stream():
    stream_name = request.form.get('stream_name')
    start_time = request.form.get('start_time')
    stop_time = request.form.get('stop_time')
    playlist_path = request.form.get('playlist')
    program = parse_playlist(playlist_path)
    timestamp = datetime.strptime(start_time, '%Y-%m-%dT%H:%M')
    program = [{'title': x['title'], 'start_time': (timestamp + timedelta(seconds=x['start_time'])).strftime('%Y-%m-%dT%H:%M')} for x in program]

    key = f"{start_time}-{stop_time}"
    stream_schedule[key] = {
        'stream_name': stream_name,
        'start_time': start_time,
        'stop_time': stop_time,
        'playlist': playlist_path,
        'program': program
    }
    schedule.append({
        'stream_name': stream_name,
        'start_time': start_time,
        'stop_time': stop_time,
        'playlist': playlist_path,
        'program': program
    })
    save_schedule()
    print(url_for('index'))
    return redirect(url_for('index'))









'''
@app.route('/')
def index():
    return render_template('index.html')'''

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_files = request.files.getlist("file")
    file_names = [file.filename for file in uploaded_files]
    # Save files if needed (optional)
    return jsonify(file_names)

@app.route('/export', methods=['POST'])
def export():
    video_list = request.json.get('videos', [])
    
    # Prepare M3U content with the proper formatting
    m3u_content = "#EXTM3U\n"
    for video in video_list:
        # Optional: add duration and title (example: 0 duration, filename as title)
        m3u_content += f"#EXTINF:0,{video}\n{video}\n"

    with open('playlist.m3u', 'w') as f:
        f.write(m3u_content)
    
    print(m3u_content)
    
    time.sleep(3) 
    return jsonify({"message": "M3U file generated successfully!"})


if __name__ == '__main__':
    port = 9999  # Default port
    #connect_to_obs()
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])  # Get port from command line argument
        except ValueError:
            print("Invalid port number. Using default port 5000.")
    
    load_schedule()
    # Start the scheduled streaming thread
    threading.Thread(target=scheduled_stream, daemon=True).start()

    app.run(debug=True, port=port)
