# Ragnar - the slow but secure way to transcribe files
Transcribe your audio and video files locally, totally secure.

![ragnar_front](https://github.com/mickekring/ragnar/assets/10948066/9729907c-8168-49b0-a67f-a2a823df6b81)

## What is this?
Ragnar is a simple app built with Python and [Streamlit](https://streamlit.io/) that transcribes your audio and video files locally on your computer, or your own server. Totally secure and without any need to call out to any services but your own computer. It uses [Whisper](https://github.com/openai/whisper) and [Whisper Stable](https://github.com/jianfch/stable-ts).
<br />The transcriptions can then be saved as txt, docx, json and srt (subtitles). You can either record audio in the app or upload files.

## How the app works - flow
1. When you run the app, a web page is opened in your default web browser.
2. You can either upload an audio/video file or record audio directly from the app.
3. When you've uploaded or recorded audio, the audio file will be converted into an mp3 file and compressed in size.
4. The mp3 file will be transcribed using Whisper locally on your computer based on your settings (language and model).
5. The transcribed text is presented to you with the possibility to download it in different formats, eg docx, txt, srt.

## Wish list - Roadmap - for the future
- [x] (v0.6.0) Add dropdown menu to choose source language of audio file - sometimes the language auto detect fails 
- [ ] Local LLM for summary and maybe chat with transcriptions
- [ ] Upload multiple files
- [ ] Create video with subtitles
- [ ] Better install instructions
- [x] (v0.6.0) Documented code :)
- [ ] Server: Queue transcriptions so that it only runs a set amount at the same time.
- [ ] Server: E-mail notice. When your transcription is done, an e-mail is sent to you with zipped files.

## Installation
This is an early beta, but it works. Expect updates as I develop this app. If you have any suggestions, feel free to ask.<br />
PS. I'm not a programmer. It's prototype code. ;) 
<br />
* Tested on Mac OSX and Windows 10 with Python 3.9 - 3.11. __3.12 won't work.__
* Download the files and 'pip install -r requirements.txt'
* Install FFMPEG on your system
* Run with 'streamlit run app.py' alternatively 'python -m streamlit run app.py'
* The first time you run it, it will take som time since the Whisper model is downloaded to your computer.

## Updates
* v0.6.0
  * I've split the code into several python files. 
  * I've fixed the 'record audio' section and it works.
  * Added a dropdown menu for language selection of the source audio. By default it's set to automatic detection, which works most of the time. But if you have people speaking with heavy accents or such you can set the language here.
* v0.5.0
  * Init upload - early beta

## Known bugs
* (v0.5.0) ~~The "record audio" section is a bit wonky~~
