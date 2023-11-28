# Ragnar - the slow but secure way to transcribe files
Transcribe your audio and video files locally, totally secure.

![ragnar_front](https://github.com/mickekring/ragnar/assets/10948066/9729907c-8168-49b0-a67f-a2a823df6b81)

## What is this?
Ragnar is a simple app that transcribes your audio and video files locally on your computer, or your own server. Totally secure and without any need to call out to any services but your own computer. It uses Whisper and Whisper Stable.
<br />The transcriptions can then be saved as txt, docx, json and srt (subtitles). You can wither record in the app or upload files.

## Wish list - for the future
* Local LLM for summary and chat with transcriptions
* Upload multiple files
* Create video with subtitles
* Better install instructions
* Documented code :) 

## Bugs
* The "record audio" section is a bit wonky

## Installation
This is an early beta, but it works. Expect a lot of updates as I develop this app. If you have any suggestions, feel free to ask.<br />
PS. I'm not a programmer. It's prototype code. ;) 
<br /><br />
* Tested on Mac OSX with Python 3.9 - 3.11
* Download the files and 'pip install -r requirements.txt'
* Install FFMPEG on your system
* Run with 'streamlit run app.py'
* The first time you run it, it will take som time since the Whisper model is downloaded to your computer.
