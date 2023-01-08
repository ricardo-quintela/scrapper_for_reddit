<p align='center'>
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/Python-3.8-yellow" />
  </a>&nbsp;&nbsp;
  <a href="https://github.com/alphacep/vosk-api">
    <img src="https://img.shields.io/static/v1?logo=GitHub&label=Repository&message=vosk-api&color=blue" />        
  </a>&nbsp;&nbsp;
  <a href="https://github.com/Zulko/moviepy">
    <img src="https://img.shields.io/static/v1?logo=GitHub&label=Repository&message=moviepy&color=blue" />        
  </a>&nbsp;&nbsp;
  <a href="https://www.reddit.com/dev/api/">
    <img src="https://img.shields.io/static/v1?logo=Reddit&label=Documentation&message=Reddit api&color=orange" />        
  </a>&nbsp;&nbsp;
  <a href="https://github.com/reddit-archive/reddit/wiki/API">
    <img src="https://img.shields.io/static/v1?logo=GitHub&label=Repository&message=Reddit api rules&color=blue" />        
  </a>&nbsp;&nbsp;
  
</p>



# Video Generator
A tool to scrape posts from reddit and generate a video from a script

# Instalation

## Requirements
This project requires [Python 3.8](https://www.python.org/downloads/)+ to work

## Cloning the repository:
```
git clone git@github.com:ricardo-quintela/scrapper_for_reddit.git
```
  
## Installing the required libraries:
```
pip install -r requirements.txt
```

## Installing a speech recognition model:  

1. [Download the model](https://alphacephei.com/vosk/models)  
2. Update the path of the model in the `settings.py` file on the MODEL_PATH variable  


# Usage
```
usage: main.py [-h] [-g] [-u] [-p] [-c] [-a] [-t] [-n] (-s | -v)

Create a video easily

optional arguments:
  -h, --help      show this help message and exit
  -g, --genaudio  save the recognized lines to a file
  -s, --scrape    scrape a post from reddit and generate a script
  -v, --video     generate a video from a background clip, an audio and a script

  -u , --user     the authorized reddit username
  -p , --post     the link of the desired post

  -c , --clip     the path to the background clip file
  -a , --audio    the path to the audio track file
  -t , --text     the path to the script file
  -n , --name     the name of the video file to be generated
```
