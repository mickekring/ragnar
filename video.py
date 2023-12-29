
### Create video


import streamlit as st
import stable_whisper
import os


def create_video(audio_file, subtitle):

	with open(audio_file, 'rb') as file:

		stable_whisper.encode_video_comparison(
			file, 
			[subtitle], 
			output_videopath='audio/audio.mp4', 
			labels=['Example 1']
			)