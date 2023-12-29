
### Translate

import streamlit as st
import stable_whisper
import json


# Function that translates audio files and creates text files

def translate_with_whisper_stable(file_name_converted, file_name, whisper_model):

    print("\nSTART: Translating with Whisper Stable")
    print(f"File: {file_name_converted}")

    progress_text = "0% översatt och klart"
    transcribe_progress_bar = st.progress(0, progress_text)

    def progress_bar(seek, total):

        sum = seek / total
        sum_percent = int(sum * 100)
        progress_text = str(sum_percent) + "% översatt och klart"
        transcribe_progress_bar.progress(sum, progress_text)

    transcribed_content_en = ""

    model = stable_whisper.load_model(whisper_model)

    result = model.transcribe(file_name_converted, task='translate', progress_callback=progress_bar, word_timestamps=False)
    
    result.save_as_json('text/' + file_name + '_en.json')


    transcribe_progress_bar.empty()

    file_json = 'text/' + file_name + '_en.json'
    extracted_texts = []

    with open(file_json, 'r') as file:
        data = json.load(file)

        for segment in data['segments']:
            extracted_texts.append(segment['text'])

    separator = "\n"
    transcribed_content_en = separator.join(extracted_texts)

    with open('text/' + file_name + '_en.txt', 'w') as file:
        # Write the string to the file
        file.write(transcribed_content_en)

    return transcribed_content_en
    