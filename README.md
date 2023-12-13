# Ragnar - the slow but secure way to transcribe files
Transcribe your audio and video files locally, totally secure.

![ragnar_front](https://github.com/mickekring/ragnar/assets/10948066/9729907c-8168-49b0-a67f-a2a823df6b81)

## What is this?
Ragnar is a simple app built with Python and [Streamlit](https://streamlit.io/) that transcribes your audio and video files locally on your computer, or your own server. Totally secure and without any need to call out to any services but your own computer. It uses [Whisper](https://github.com/openai/whisper) and [Whisper Stable](https://github.com/jianfch/stable-ts).
<br />The transcriptions can then be saved as txt, docx, json and srt (subtitles). You can either record audio in the app or upload files.

## Wish list - Roadmap - for the future
- [ ] Add dropdown menu to choose source language of audio file - sometimes the language auto detect fails 
- [ ] Local LLM for summary and maybe chat with transcriptions
- [ ] Upload multiple files
- [ ] Create video with subtitles
- [ ] Better install instructions
- [ ] Documented code :)
- [ ] Server: Queue transcriptions so that it only runs a set amount at the same time.
- [ ] Server: E-mail notice. When your transcription is done, an e-mail is sent to you with zipped files.

## Installation
This is an early beta, but it works. Expect a lot of updates as I develop this app. If you have any suggestions, feel free to ask.<br />
PS. I'm not a programmer. It's prototype code. ;) 
<br />
* Tested on Mac OSX with Python 3.9 - 3.11
* Tested on Windows (user feedback) - unknown versions of Python.
* Download the files and 'pip install -r requirements.txt'
* Install FFMPEG on your system
* Run with 'streamlit run app.py'
* The first time you run it, it will take som time since the Whisper model is downloaded to your computer.

## Updates
* v0.5.0 - init upload - early beta

## Known bugs
* The "record audio" section is a bit wonky
