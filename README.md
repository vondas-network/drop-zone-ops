<p align="center">
  <img width="40%" height="40%" src="https://github.com/user-attachments/assets/e3551d8c-dce3-4b38-be46-631013c78e06"/>  
</p>

<p align="center"><em>Taking streaming to new heights!</em></p> 

## What is this?
An automation project focused on streamlining the m3u creation process with the Open Broadcast Software API & WebSockets. 

<p align="left">
  <img width="55%" height="55%" src="https://github.com/user-attachments/assets/004a37a7-f267-46a4-9684-e0a27ac535cd"/>  
</p>

## How does it work? 

Once the server is running, go to _http://localhost:9999_

<p align="left">
  <img width="55%" height="55%" src="https://github.com/user-attachments/assets/8fc34706-f0a5-4173-8edd-3d831f032515"/>  
</p>

Place files in the drop zone or click "Upload Folder" to upload content manually

<p align="left">
  <img width="55%" height="55%" src="https://github.com/user-attachments/assets/5a8dedca-5102-4b9a-b7cb-42685286445f"/>  
</p>

Export m3U file to the root directory, example below

``` bash
#EXTM3U
#EXTINF:0,highlight_video.mp4
highlight_video.mp4
#EXTINF:0,replay_video.mp4
replay_video.mp4
```

Schedule your stream

<p align="left">
  <img width="55%" height="55%" src="https://github.com/user-attachments/assets/4add66dd-4ce1-40cc-92eb-cea1b7e98b6b"/>  
</p>


Once the stream is scheduled it will refresh the page and appear below
<p align="left">
  <img width="55%" height="55%" src="https://github.com/user-attachments/assets/5298e22d-eb81-45ba-a1db-ef214a7f8e38"/>  
</p>

A new OBS _scene_ is created with _VLC_ as a source when the scheduled time happens

<p align="left">
  <img width="55%" height="55%" src="https://github.com/user-attachments/assets/a6431c57-c941-42f1-a0dd-163e2e46214e"/>  
</p>


## Project setup

### Linux & MacOS 

#### Install VLC
Download VLC [here](https://www.videolan.org/)

#### Install the project requirements
``` bash
pip install -r requirements.txt
```

#### Create Python virtual environment
In a nutshell, Python virtual environments help decouple and isolate Python installs and associated pip packages. This allows end-users to install and manage their own set of packages that are independent of those provided by the system or used by other projects.
```bash
 cd videobeaux
 python -m venv env
```

### Activate Python virtual environment
This will activate your virtual environment. Immediately, you will notice that your terminal path includes env, signifying an activated virtual environment.

``` bash
source env/bin/activate
```

### Windows 11/10

#### Install VLC
Download VLC [here](https://www.videolan.org/) (* 64-bit only)


#### Install the project requirements
``` bash
pip install -r requirements.txt
```

## Video Demo
https://github.com/user-attachments/assets/0ff4bf5c-e9e2-4d63-a5da-1fbda08663aa

## Current Bugs
- Video files _need_ to be in the root directory to properly encode as m3u8 playlist
- Remove older streams from the schedule

## Testing
- Windows: 11 & 10 (64-bit only) 
- Linux: Ubuntu 24.04
- MacOS: M1 Apple Silicon
