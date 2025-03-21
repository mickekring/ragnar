# Ragnar - the slow but secure way to transcribe files
Transcribe your audio and video files locally, totally secure.

![ragge_header](https://github.com/user-attachments/assets/fbb54afb-ec4a-462f-b24f-c3ee056e3ea8)

## What is this?
Ragnar is a simple app built with Python and [Streamlit](https://streamlit.io/) that transcribes your audio and video files locally on your computer, or your own server. Totally secure and without any need to call out to any services but your own computer. It uses [Whisper](https://github.com/openai/whisper) and [KB Whisper (from Kungliga Biblioteket)](https://huggingface.co/collections/KBLab/kb-whisper-67af9eafb24da903b63cc4aa).
<br />The transcriptions can then be saved as txt, docx, json and srt (subtitles). 

## How the app works - flow
1. When you run the app, a web page is opened in your default web browser.
2. You upload an audio- or video file directly from the app.
3. When you've uploaded audio, the audio file will be converted into an mp3 file and compressed in size.
4. The mp3 file will be transcribed using Whisper or KB Whisper locally on your computer based on your settings (language and model).
5. The transcribed text is presented to you with the possibility to download.

## Installation
This is an early beta, but it works. Expect updates as I develop this app. If you have any suggestions, feel free to ask.<br />
PS. I'm not a programmer. It's prototype code. ;) 
<br />
* Tested on Mac OSX and Windows 10 with Python 3.12
* Download the files and 'pip install -r requirements.txt'
* Install FFMPEG on your system
* Run with 'streamlit run app.py' alternatively 'python -m streamlit run app.py'
* The first time you run it, it will take som time since the Whisper model is downloaded to your computer.
* If you're on Windows, I included a 'ragnar.bat' file which starts the application if you place all code in 'C:\ragnar'. You can edit this if you place Ragnar in a different folder.

## Updates
* v0.7.2
  * Just added some files for deployment to Docker
* v0.7.0
  * Partially rewritten. Make sure to update your pip packages from requirement.txt if you've already installed Ragnar
  * Added KB (Kungliga Bibliotekets fine tuned Whisper) Whisper and reverted back to vanilla Whisper from OpenAI. Still all local
  * Removed translation which a language model does a lot better
* v0.6.2
  * Updated requirements.txt and tested with latest versions of eg Streamlit
  * Tidying up and moving functions to separate folder
  * Replaced the audio recorder with Streamlit's new audio recorder
* v0.6.1
  * Windows users getting weird characters instead of å ä ö. Fixed it with utf-8 in transcribe.py
* v0.6.0
  * I've split the code into several python files. 
  * I've fixed the 'record audio' section and it works.
  * Added a dropdown menu for language selection of the source audio. By default it's set to automatic detection, which works most of the time. But if you have people speaking with heavy accents or such you can set the language here.
* v0.5.0
  * Init upload - early beta

## Known bugs
* (v0.5.0) ~~The "record audio" section is a bit wonky~~

## License
Some of you have asked why I haven't added a license to Ragnar. The truth is that I have no knowledge about licensing and open source. I've got some suggestions like MIT, and I'm looking into it.  
My point is that Ragnar is free to use, modify, distribute and do what you want with as long as you want to. It's just code that I wrote to solve an issue me and my collegues had. If it helps more people, great.  

## Support
Unfortunately, it's not possible for me to assist you guys with support. I just don't have the time. Report bugs and problems and hopefully we can try to solve them together.  


