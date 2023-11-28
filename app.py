
### Ragnar
app_version = "0.5.0"
### Author: Micke Kring
### Contact: mikael.kring@ri.se


import os
import streamlit as st
from pydub import AudioSegment
from datetime import datetime
#from sys import platform
import json
from docx import Document
import hashlib
from audiorecorder import audiorecorder
import stable_whisper

# Checks OS

#if platform == "linux" or platform == "linux2":
#    operativsystem = "linux"
#elif platform == "darwin":
#    operativsystem = "macos"
#elif platform == "win32":
#    operativsystem = "windows"


### INITIAL VARIABLES

# Creates folder if they don't exist
os.makedirs("audio", exist_ok=True) # Where user puts its audio/video file for transcription
os.makedirs("text", exist_ok=True) # Where transcribed document are beeing stored


# Check and set default values if not set in session_state
if "translation" not in st.session_state:
    st.session_state["translation"] = False
if "cpu_vs_gpu" not in st.session_state:
    st.session_state["cpu_vs_gpu"] = False
if "spoken_language" not in st.session_state:
    st.session_state["spoken_language"] = "Svenska"
if "transcribe_model" not in st.session_state:
    st.session_state["transcribe_model"] = "Stor (bäst kvalitet)"
if "debug_code" not in st.session_state:
    st.session_state["debug_code"] = False
if "file_name_converted" not in st.session_state:
    st.session_state["file_name_converted"] = None


# Automatically sets device to either CPU or GPU

#if st.session_state["debug_code"]:
#    device = "cuda:0" if torch.cuda.is_available() else "cpu"
#    print(device)

# --- --- --- --- --- --- --- --- --- ---



def compute_file_hash(uploaded_file):

    if st.session_state["debug_code"]:
        print("\n--- --- --- ---\nDebug: compute_file_hash")

    # Compute the MD5 hash of a file
    hasher = hashlib.md5()
    for chunk in iter(lambda: uploaded_file.read(4096), b""):
        hasher.update(chunk)
    uploaded_file.seek(0)  # Reset the file pointer to the beginning
    return hasher.hexdigest()



def convert_to_mono_and_compress(uploaded_file, file_name, target_size_MB=22):

    if st.session_state["debug_code"]:
        print("\n--- --- --- ---\nDebug: convert_to_mono_and_compress")

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



def transcribe_with_whisper_stable(file_name_converted, file_name):

    if st.session_state["debug_code"]:
        print("\n--- --- --- ---\nDebug:transcribe_with_whisper_stable")

    progress_text = "0% transkriberat och klart"
    transcribe_progress_bar = st.progress(0, progress_text)

    def progress_bar(seek, total):

        sum = seek / total
        sum_percent = int(sum * 100)
        progress_text = str(sum_percent) + "% transkriberat och klart"
        transcribe_progress_bar.progress(sum, progress_text)

    transcribed_content = ""

    model = stable_whisper.load_model(model_map_transcribe_model[st.session_state["transcribe_model"]])
    print(model_map_transcribe_model[st.session_state["transcribe_model"]])

    result = model.transcribe(file_name_converted, progress_callback=progress_bar)
    
    result.to_srt_vtt('text/' + file_name + '.srt', word_level=False)
    result.save_as_json('text/' + file_name + '.json')


    transcribe_progress_bar.empty()

    file_json = 'text/' + file_name + '.json'
    extracted_texts = []

    with open(file_json, 'r') as file:
        data = json.load(file)

        for segment in data['segments']:
            extracted_texts.append(segment['text'])

    separator = "\n"
    transcribed_content = separator.join(extracted_texts)

    with open('text/' + file_name + '.txt', 'w') as file:
        # Write the string to the file
        file.write(transcribed_content)


    return transcribed_content



def translate_with_whisper_stable(file_name_converted, file_name):

    if st.session_state["debug_code"]:
        print("\n--- --- --- ---\nDebug:translate_with_whisper_stable")

    progress_text = "0% översatt och klart"
    transcribe_progress_bar = st.progress(0, progress_text)

    def progress_bar(seek, total):

        sum = seek / total
        sum_percent = int(sum * 100)
        progress_text = str(sum_percent) + "% översatt och klart"
        transcribe_progress_bar.progress(sum, progress_text)

    transcribed_content_en = ""

    model = stable_whisper.load_model(model_map_transcribe_model[st.session_state["transcribe_model"]])

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



### MAIN APP ###########################



def main():

    global translation
    global model_map_transcribe_model


    ### SIDEBAR

    #st.sidebar.markdown("# Ragnar")
    st.sidebar.image("images/ragge3.png", width = 220)

    ###### SIDEBAR SETTINGS

    st.sidebar.header("Inställningar")
    st.sidebar.markdown("")


    transcribe_model = st.sidebar.selectbox(
            "Välj modell för transkribering", 
            ["Stor (bäst kvalitet)", "Medium", "Bas (sämst kvalitet)"],
            index=["Stor (bäst kvalitet)", "Medium", "Bas (sämst kvalitet)"].index(st.session_state["transcribe_model"]),
        )


    model_map_transcribe_model = {
            "Bas (sämst kvalitet)": "base",
            "Medium": "medium",
            "Stor (bäst kvalitet)": "large"
        }

    # Update the session_state directly
    st.session_state["transcribe_model"] = transcribe_model

    #number_of_speakers = st.sidebar.number_input("Antal talare", value = 1)
    #st.sidebar.markdown("#")

    translation = st.sidebar.toggle(
        "Översättning engelska", 
        help = "Transkriberar text på orgnialspråk, men skapar även en översättning till engelska"
        )

    st.sidebar.markdown(
        "#"
        )

    debug_code = st.sidebar.toggle(
        "Debug"
        )

    # Update the session_state directly
    st.session_state["translation"] = translation
    st.session_state["debug_code"] = debug_code

     
    ### ### ### ### ### ### ### ### ### ### ###
    ### MAIN PAGE
    ###
    ### ### ###

    st.markdown("""
        # Ragnar
        ### Din GDPR- och sekretessäkrade transkriberare
        """)


    # CREATE TWO TABS FOR FILE UPLOAD VS RECORDED AUDIO    

    tab1, tab2 = st.tabs(["Ladda upp", "Spela in"])


    # FILE UPLOADER

    with tab1:
        
        uploaded_file = st.file_uploader(
            "Ladda upp din ljud- eller videofil här",
            type=["mp3", "wav", "flac", "mp4", "m4a", "aifc"],
            help="Max 2GB stora filer", label_visibility="collapsed",
            )


        if uploaded_file:

            current_file_hash = compute_file_hash(uploaded_file)

            # If the uploaded file hash is different from the one in session state, reset the state
            if "file_hash" not in st.session_state or st.session_state.file_hash != current_file_hash:
                st.session_state.file_hash = current_file_hash
                if "transcribed" in st.session_state:
                    del st.session_state.transcribed

            if "transcribed" not in st.session_state:

                with st.spinner('Din ljudfil är lite stor. Jag ska bara komprimera den lite först...'):
                    print("Compressing audio")
                    st.session_state.file_name_converted = convert_to_mono_and_compress(uploaded_file, uploaded_file.name)
                    st.success('Inspelning komprimerad och klar. Startar transkribering.')

                with st.spinner('Transkriberar. Det här kan ta ett litet tag beroende på hur lång inspelningen är...'):
                    print("Transcribing audio")
                    st.session_state.transcribed = transcribe_with_whisper_stable(st.session_state.file_name_converted, uploaded_file.name)
                    st.success('Transkribering klar.')

                    st.balloons()

                if st.session_state["translation"]:
                    with st.spinner('Översätter. Det här kan ta ett litet tag beroende på hur lång inspelningen är...'):
                        print("Translating audio")
                        st.session_state.transcribed_en = translate_with_whisper_stable(st.session_state.file_name_converted, uploaded_file.name)
                        st.success('Översättning klar.')

                        st.balloons()

            
            if st.session_state["translation"]:
                document = Document()
                document.add_paragraph(st.session_state.transcribed_en)

                document.save('text/' + uploaded_file.name + '_en.docx')

                with open("text/" + uploaded_file.name + "_en.docx", "rb") as template_file_en:
                    template_byte_en = template_file_en.read()


            document = Document()
            document.add_paragraph(st.session_state.transcribed)

            document.save('text/' + uploaded_file.name + '.docx')

            with open("text/" + uploaded_file.name + ".docx", "rb") as template_file:
                template_byte = template_file.read()



            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                with open('text/' + uploaded_file.name + '.txt', "rb") as file_txt:
                    st.download_button(
                        label = ":flag-se: Ladda ned text",
                        data = file_txt,
                        file_name = uploaded_file.name + '.txt',
                        mime = 'text/plain',
                    )

            with col2:
                st.download_button(
                    label = ":flag-se: Ladda ned word",
                    data = template_byte,
                    file_name = uploaded_file.name + '.docx',
                    mime = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                )

            with col3:
                with open('text/' + uploaded_file.name + '.srt', "rb") as file_srt:
                    st.download_button(
                        label = ":flag-se: Ladda ned srt",
                        data = file_srt,
                        file_name = uploaded_file.name + '.srt',
                        mime = 'text/plain',
                    )

            with col4:
                with open('text/' + uploaded_file.name + '.json', "rb") as file_json:
                    st.download_button(
                        label = ":flag-se: Ladda ned json",
                        data = file_json,
                        file_name = uploaded_file.name + '.json',
                        mime = 'application/json',
                    )

            if st.session_state["translation"]:

                col5, col6, col7, col8 = st.columns(4)

                with col5:
                    with open('text/' + uploaded_file.name + '_en.txt', "rb") as file_txt:
                        st.download_button(
                            label = ":flag-gb: Download text",
                            data = file_txt,
                            file_name = uploaded_file.name + '_en.txt',
                            mime = 'text/plain',
                        )

                with col6:
                    st.download_button(
                        label = ":flag-gb: Download word",
                        data = template_byte_en,
                        file_name = uploaded_file.name + '_en.docx',
                        mime = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                    )

            
            st.markdown("### Transkribering")
            
            if st.session_state.file_name_converted is not None:
                st.audio(st.session_state.file_name_converted, format='audio/wav')
            
            st.write(st.session_state.transcribed)

    
    # AUDIO RECORDER ###### ###### ######

    with tab2:
        
        audio = audiorecorder(start_prompt="Spela in", stop_prompt="Stoppa", pause_prompt="", key=None)

    
        if len(audio) > 0:

            # To save audio to a file, use pydub export method:
            audio.export("audio/local_recording.wav", format="wav")
            
            with st.spinner('Din ljudfil är lite stor. Jag ska bara komprimera den lite först...'):
                print("Compressing audio")
                st.session_state.file_name_converted = convert_to_mono_and_compress("audio/local_recording.wav", "local_recording.wav")
                st.success('Inspelning komprimerad och klar. Startar transkribering.')

            with st.spinner('Transkriberar. Det här kan ta ett litet tag beroende på hur lång inspelningen är...'):
                print("Transcribing audio")
                st.session_state.transcribed = transcribe_with_whisper_stable(st.session_state.file_name_converted, "local_recording.mp3")
                local_recording_name = "local_recording.mp3"
                st.success('Transkribering klar.')

            if st.session_state["translation"]:
                with st.spinner('Översätter. Det här kan ta ett litet tag beroende på hur lång inspelningen är...'):
                    print("Translating audio")
                    st.session_state.transcribed_en = translate_with_whisper_stable(st.session_state.file_name_converted, "local_recording.mp3")
                    st.success('Översättning klar.')

                    st.balloons()

            if st.session_state["translation"]:
                document = Document()
                document.add_paragraph(st.session_state.transcribed_en)

                document.save('text/' + uploaded_file.name + '_en.docx')

                with open("text/" + uploaded_file.name + "_en.docx", "rb") as template_file_en:
                    template_byte_en = template_file_en.read()


            document = Document()
            document.add_paragraph(st.session_state.transcribed)

            document.save('text/' + local_recording_name + '.docx')

            with open("text/local_recording.mp3.docx", "rb") as template_file:
                template_byte = template_file.read()

            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                with open('text/' + local_recording_name + '.txt', "rb") as file_txt:
                    st.download_button(
                        label = "Ladda ned text",
                        data = file_txt,
                        file_name = local_recording_name + '.txt',
                        mime = 'text/plain',
                    )

            with col2:
                st.download_button(
                    label = "Ladda ned word",
                    data = template_byte,
                    file_name = local_recording_name + '.docx',
                    mime = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                )

            with col3:
                with open('text/' + local_recording_name+ '.srt', "rb") as file_srt:
                    st.download_button(
                        label = "Ladda ned srt",
                        data = file_srt,
                        file_name = local_recording_name + '.srt',
                        mime = 'text/plain',
                    )

            with col4:
                with open('text/' + local_recording_name + '.json', "rb") as file_json:
                    st.download_button(
                        label = "Ladda ned json",
                        data = file_json,
                        file_name = local_recording_name + '.json',
                        mime = 'application/json',
                    )

            if st.session_state["translation"]:

                col5, col6, col7, col8 = st.columns(4)

                with col5:
                    with open('text/' + local_recording_name + '_en.txt', "rb") as file_txt:
                        st.download_button(
                            label = ":flag-gb: Download text",
                            data = file_txt,
                            file_name = local_recording_name + '_en.txt',
                            mime = 'text/plain',
                        )

                with col6:
                    st.download_button(
                        label = ":flag-gb: Download word",
                        data = template_byte_en,
                        file_name = local_recording_name + '_en.docx',
                        mime = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                    )

            
            st.markdown("### Transkribering")
            
            if st.session_state.file_name_converted is not None:
                st.audio(st.session_state.file_name_converted, format='audio/wav')
            
            st.write(st.session_state.transcribed)



if __name__ == "__main__":
    main()



