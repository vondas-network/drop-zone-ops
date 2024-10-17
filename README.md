# drop-zone-ops

<p align="center">
  <img width="45%" height="45%" src="https://github.com/vondas-network/videobeaux/blob/main/img/videobeaux-1.png?raw=true"/>  
</p>

<p align="center"><em>Your friendly multilateral video toolkit built for artists by artists. It's your best friend.</em></p> 


## Dependencies
FFmpeg is required for the project. Install *ffmpeg* using [Homebrew](https://formulae.brew.sh/formula/ffmpeg)
```bash
brew install ffmpeg
```

## Requirements

Install the project requirements
``` bash
pip install -r requirements.txt
```

## Project setup

### Create Python virtual environment
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
