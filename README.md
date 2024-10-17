<p align="center">
  <img width="40%" height="40%" src="https://github.com/user-attachments/assets/e3551d8c-dce3-4b38-be46-631013c78e06"/>  
</p>

<p align="center"><em>Taking streaming to new heights!</em></p> 

## What is this?
An automation project focused on streamlining the m3u creation process with the Open Broadcast Software API & WebSockets

<p align="left">
  <img width="50%" height="50%" src="https://github.com/user-attachments/assets/84709b52-4b5b-41b0-8ba9-6aed5f238d65"/>  
</p>

## Video Demo

https://github.com/user-attachments/assets/0ff4bf5c-e9e2-4d63-a5da-1fbda08663aa

## How does it work? 
Place files in the drop zone or click "Upload Files" to upload content manually
<p align="left">
  <img width="55%" height="55%" src="https://github.com/user-attachments/assets/929e3a4d-54e3-4eab-90cc-49447072ac97"/>  
</p>

Export m3U file and create OBS event
<img width="462" alt="Screenshot 2024-10-17 at 17 09 32" src="https://github.com/user-attachments/assets/a33b454c-a6be-4cf1-ad96-53887a6b52c7">

Look for the success message
<img width="1389" alt="Screenshot 2024-10-17 at 17 11 00" src="https://github.com/user-attachments/assets/1b3e287f-0eae-4189-80b9-50864ffc40d2">

A new OBS _scene_ is created with _VLC_ as a source
<img width="1432" alt="Screenshot 2024-10-17 at 17 07 40" src="https://github.com/user-attachments/assets/a6431c57-c941-42f1-a0dd-163e2e46214e">

## Project setup

Tested on: 
- Windows: 11 & 10 (64-bit only) 
- Linux: Ubuntu 24.04
- MacOS: M1 Apple Silicon

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

### Activate Virtual Environment
This will activate your virtual environment. Immediately, you will notice that your terminal path includes env, signifying an activated virtual environment.

``` bash
source env/bin/activate
```

### Windows 11/10

#### Install the project requirements
``` bash
pip install -r requirements.txt
```
