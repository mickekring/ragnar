
### Transcribe

import streamlit as st
import stable_whisper
import json


# Functions that transcribes audio and creates the text files

def transcribe_with_whisper_stable(file_name_converted, file_name, whisper_model, spoken_language):

	print("\nSTART: Transcribing with Whisper Stable")
	print(f"File: {file_name_converted}")
	print(f"Spoken language: {spoken_language}")

	progress_text = "0% transkriberat och klart"
	transcribe_progress_bar = st.progress(0, progress_text)

	def progress_bar(seek, total):

		sum = seek / total
		sum_percent = int(sum * 100)
		progress_text = str(sum_percent) + "% transkriberat och klart"
		transcribe_progress_bar.progress(sum, progress_text)

	transcribed_content = ""

	model = stable_whisper.load_model(whisper_model)
	print(f"Whisper model: {whisper_model}\n")

	result = model.transcribe(file_name_converted, progress_callback=progress_bar, language=spoken_language)

	result.to_srt_vtt('text/' + file_name + '.srt', word_level=False)
	result.save_as_json('text/' + file_name + '.json')

	transcribe_progress_bar.empty()

	file_json = 'text/' + file_name + '.json'
	extracted_texts = []

	with open(file_json, 'r', encoding='utf-8') as file:
		data = json.load(file)

		for segment in data['segments']:
			extracted_texts.append(segment['text'])

	separator = "\n"
	transcribed_content = separator.join(extracted_texts)

	with open('text/' + file_name + '.txt', 'w') as file:
		# Write the string to the file
		file.write(transcribed_content)

	print("\nDONE: Transcribing with Whisper Stable")

	return transcribed_content
