
### Functions

import streamlit as st
from pydub import AudioSegment


# Converts and compresses audio or video file to mp3 and a more manageble size

def convert_to_mono_and_compress(uploaded_file, file_name, target_size_MB=22):

    global file_name_converted

    # Load the audio file
    audio = AudioSegment.from_file(uploaded_file)

    # Convert to mono
    audio = audio.set_channels(1)

    # Calculate target bitrate to achieve the desired file size (in bits per second)
    duration_seconds = len(audio) / 1000.0  # pydub works in milliseconds
    target_bitrate = int((target_size_MB * 1024 * 1024 * 8) / duration_seconds)

    # Compress the audio file
    try:
        audio.export("audio/" + file_name + ".mp3", format="mp3", bitrate=f"{target_bitrate}")
        file_name_converted = "audio/" + file_name + ".mp3"
        
    except Exception as e:
        print(f"Error during audio export: {e}")
        return None

    return file_name_converted
