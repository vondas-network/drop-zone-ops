import json
import requests
from obswebsocket import obsws, events

# Connection details for OBS WebSocket
OBS_HOST = "localhost"
OBS_PORT = 4455
OBS_PASSWORD = "your_password"

# Owncast server URL (change to your actual endpoint)
OWNCAST_URL = "https://schwwaaa.net/api/status"
headers = {"Authorization": "Bearer ="}

# Load the M3U playlist and parse file information
def parse_m3u(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        # Extract only the file paths, ignoring other m3u metadata
        return [line.strip() for line in lines if not line.startswith("#")]

# Get the list of files from the m3u file
m3u_files = parse_m3u(r"D:\scripting\dropzone-win\playlist.m3u")

# Function to send HTTP request to Owncast
def send_owncast_request(file_name):
    data = {
        'filename': file_name
    }
    response = requests.get(OWNCAST_URL, json=data, headers=headers)
    print(response.status_code)
    if response.status_code == 200:
        print(f"Successfully sent data for {file_name}")
    else:
        print(f"Failed to send data for {file_name}: {response.status_code}")

# Function to find the file that matches the playback event
def get_current_file(m3u_files, current_index):
    if 0 <= current_index < len(m3u_files):
        return m3u_files[current_index]
    return None

# Track the current index of the file playing
current_index = -1

# WebSocket event handler
def on_media_playback_started(message):
    global current_index
    # Increment to get the next file in the playlist
    current_index += 1
    current_file = get_current_file(m3u_files, current_index)
    print(f"CURRENT FILE::  {current_file}")
    
    if current_file:
        print(f"Now playing: {current_file}")
        send_owncast_request(current_file)
    else:
        print("No more files in the playlist.")

# Connect to OBS WebSocket
ws = obsws(OBS_HOST, OBS_PORT, OBS_PASSWORD)
ws.connect()

# Register event listener
ws.register(on_media_playback_started, events.MediaInputPlaybackStarted)

try:
    # Keep the WebSocket connection open
    print("Listening for events...")
    while True:
        pass
except KeyboardInterrupt:
    ws.disconnect()