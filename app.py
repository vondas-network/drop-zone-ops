from flask import Flask, render_template, request, jsonify
from obswebsocket import obsws, requests, exceptions
import os
import sys
import time

# Define connection parameters
host = 'localhost'
port = 4455
password = 'password'

# Define source details
scene_name = "MyNewScene"
source_name = "MyImageSource"
image_path = os.path.abspath("image.png")

MEDIA_FILE = "/Users/rr/Desktop/obs/dropzone/playlist.m3u"  # Change to your VLC media source path


# Initialize OBS WebSocket connection
ws = obsws(host=host, port=port, password=password)

app = Flask(__name__)

def connect_to_obs():
    """Connect to OBS."""
    try:
        ws.connect()
        print("Connected to OBS WebSocket server.")
    except exceptions.ConnectionFailure:
        print("Failed to connect to OBS WebSocket server.")
    except exceptions.AuthenticationFailure:
        print("Authentication failed. Check your password.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def create_scene_with_image():
    """Create a new scene and add an image source to it."""
    try:
        # Create a new scene
        ws.call(requests.CreateScene(sceneName=scene_name))
        print(f"Scene '{scene_name}' created.")
        time.sleep(1)

        # Add the image source to the scene
        response = ws.call(requests.CreateInput(
            sceneName=scene_name,
            inputName=source_name,
            inputKind="vlc_source",
            inputSettings={
                "playlist": [{"hidden": False, "selected": False, "value": MEDIA_FILE}],
                "loop": True  # Optional: set to loop the playlist
            }
        ))
        print(f"Image source '{scene_name}' added with image path '{image_path}'.")

        # Get the scene item ID for the image source
        scene_item_id = response.datain.get("sceneItemId")
        
        # Set the current program scene to the new scene
        ws.call(requests.SetCurrentProgramScene(sceneName=SCENE_NAME))

        # Get the source's scene item ID
        scene_item_list = ws.call(requests.GetSceneItemList(sceneName=SCENE_NAME)).getSceneItems()
        vlc_source_item_id = next(item['sceneItemId'] for item in scene_item_list if item['sourceName'] == SOURCE_NAME)

        # Fit the VLC source to the screen dimensions
        screen_width = 1920  # Example width
        screen_height = 1080  # Example height
        ws.call(requests.SetSceneItemTransform(
            sceneName=SCENE_NAME,
            sceneItemId=vlc_source_item_id,

            sceneItemTransform={
                'boundsWidth': 1920, 
                'boundsHeight': 1080, 
                'boundsType': 'OBS_BOUNDS_SCALE_INNER'
            }
        ))

        print(f"Scene '{SCENE_NAME}' created with VLC source '{SOURCE_NAME}' and fitted to screen.")
        
    except Exception as e:
        print(f"Failed to create scene or add source: {e}")
    finally:
        # Ensure we disconnect from OBS when done
        ws.disconnect()
        print("Disconnected from OBS WebSocket server.")

@app.route('/')
def index():
    return render_template('index.html')

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
    create_scene_with_image()
    return jsonify({"message": "M3U file generated successfully!"})


if __name__ == '__main__':
    port = 9999  # Default port
    connect_to_obs()
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])  # Get port from command line argument
        except ValueError:
            print("Invalid port number. Using default port 5000.")
    
    app.run(debug=True, port=port)
