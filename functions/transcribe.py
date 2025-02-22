
### Transcribe

import streamlit as st
import torch
from datasets import load_dataset
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import whisper

# Functions that transcribes audio and creates the text files

def transcribe_with_kb_whisper(file_name_converted, file_name, whisper_model, spoken_language):
	
	device = "cuda:0" if torch.cuda.is_available() else "cpu"
	torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
	model_id = f"KBLab/{whisper_model}"

	model = AutoModelForSpeechSeq2Seq.from_pretrained(
		model_id, torch_dtype=torch_dtype, use_safetensors=True, cache_dir="cache"
	)
	model.to(device)
	processor = AutoProcessor.from_pretrained(model_id)

	pipe = pipeline(
		"automatic-speech-recognition",
		model=model,
		tokenizer=processor.tokenizer,
		feature_extractor=processor.feature_extractor,
		torch_dtype=torch_dtype,
		device=device,
	)

	generate_kwargs = {"task": "transcribe", "language": spoken_language}
	
	res = pipe(file_name_converted, 
			chunk_length_s=30,
			generate_kwargs={"task": "transcribe", "language": spoken_language})

	transcribed_content = res["text"]

	with open('text/' + file_name + '.txt', 'w') as file:
		# Write the string to the file
		file.write(transcribed_content)
	
	return transcribed_content


def transcribe_with_whisper(file_name_converted, file_name, whisper_model, spoken_language):

	transcribed_content = ""

	model = whisper.load_model(whisper_model)
	result = model.transcribe(file_name_converted, language=spoken_language)
	transcribed_content = result["text"]

	with open('text/' + file_name + '.txt', 'w') as file:
		# Write the string to the file
		file.write(transcribed_content)

	return transcribed_content
