
# Python imports
import os
import streamlit as st
import hashlib

# External imports
from docx import Document
from pydub import AudioSegment

# Local imports
from functions.functions import convert_to_mono_and_compress
from functions.transcribe import transcribe_with_whisper_stable
from functions.translate import translate_with_whisper_stable
import config as c


print("\n\n--- --- --- ---\nSTART: App start")


### INITIAL VARIABLES

# Creates folder if they don't exist
os.makedirs("audio", exist_ok=True) # Where audio/video files are stored for transcription
os.makedirs("text", exist_ok=True) # Where transcribed document are beeing stored


# Check and set default values if not set in session_state
# of Streamlit
if "translation" not in st.session_state: # If audio has been translated
    st.session_state["translation"] = False
if "cpu_vs_gpu" not in st.session_state: # If user device has GPU support
    st.session_state["cpu_vs_gpu"] = False
if "spoken_language" not in st.session_state: # What language source audio is in
    st.session_state["spoken_language"] = "Automatiskt"
if "transcribe_model" not in st.session_state: # What model of Whisper to use
    st.session_state["transcribe_model"] = "Stor (bäst kvalitet)"
if "file_name_converted" not in st.session_state: # Audio file name
    st.session_state["file_name_converted"] = None


# Checking if uploaded or recorded audio file has been transcribed
def compute_file_hash(uploaded_file):

    print("\nSTART: Check if audio file has been transcribed - hash")

    # Compute the MD5 hash of a file
    hasher = hashlib.md5()
    
    for chunk in iter(lambda: uploaded_file.read(4096), b""):
        hasher.update(chunk)
    uploaded_file.seek(0)  # Reset the file pointer to the beginning

    print("DONE: Check if audio file has been transcribed - hash")
    
    return hasher.hexdigest()



### MAIN APP ###########################


# Page configuration
st.set_page_config(
    page_title="Ragnar",
    page_icon=None,
    layout="centered",
    initial_sidebar_state="auto"
    )



def main():

    global translation
    global model_map_transcribe_model


    ### SIDEBAR

    # Sidebar image of Ragnar
    st.sidebar.image("images/ragge3.png", width = 220)

    ###### SIDEBAR SETTINGS

    st.sidebar.header("Inställningar")
    st.sidebar.markdown("")

    # Dropdown menu - choose Whisper model
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

    # Dropdown menu - choose source language of audio
    spoken_language = st.sidebar.selectbox(
            "Välj språk som talas", 
            ["Automatiskt", "Svenska", "Engelska", "Franska", "Tyska", "Spanska"],
            index=["Automatiskt", "Svenska", "Engelska", "Franska", "Tyska", "Spanska"].index(st.session_state["spoken_language"]),
        )

    model_map_spoken_language = {
            "Automatiskt": None,
            "Svenska": "sv",
            "Engelska": "en",
            "Franska": "fr",
            "Tyska": "de",
            "Spanska": "sp"

        }

    # Update the session_state directly
    st.session_state["transcribe_model"] = transcribe_model
    st.session_state["spoken_language"] = spoken_language

    #Toggle switch for tranlation to english, if source audio is not in english
    translation = st.sidebar.toggle(
        "Översättning engelska", 
        help = "Transkriberar text på orgnialspråk, men skapar även en översättning till engelska"
        )

    st.sidebar.markdown(
        "#"
        )

    # Update the session_state directly
    st.session_state["translation"] = translation

    st.sidebar.markdown(f"""
    Version: {c.app_version}
                        """)



    ### MAIN PAGE

    # Title
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

            # Checks if uploaded file has already been transcribed
            current_file_hash = compute_file_hash(uploaded_file)

            # If the uploaded file hash is different from the one in session state, reset the state
            if "file_hash" not in st.session_state or st.session_state.file_hash != current_file_hash:
                st.session_state.file_hash = current_file_hash
                
                if "transcribed" in st.session_state:
                    del st.session_state.transcribed

            
            # If audio has not been transcribed
            if "transcribed" not in st.session_state:

                # Sends audio to be converted to mp3 and compressed
                with st.spinner('Din ljudfil är lite stor. Jag ska bara komprimera den lite först...'):
                    st.session_state.file_name_converted = convert_to_mono_and_compress(uploaded_file, uploaded_file.name)
                    st.success('Inspelning komprimerad och klar. Startar transkribering.')

               # Transcribes audio with Whisper
                with st.spinner('Transkriberar. Det här kan ta ett litet tag beroende på hur lång inspelningen är...'):
                    st.session_state.transcribed = transcribe_with_whisper_stable(st.session_state.file_name_converted, 
                        uploaded_file.name, 
                        model_map_transcribe_model[st.session_state["transcribe_model"]],
                        model_map_spoken_language[st.session_state["spoken_language"]])
                    st.success('Transkribering klar.')

                    st.balloons()

                # If translation switch is on, translates audio
                if st.session_state["translation"]:
                    with st.spinner('Översätter. Det här kan ta ett litet tag beroende på hur lång inspelningen är...'):
                        st.session_state.transcribed_en = translate_with_whisper_stable(st.session_state.file_name_converted, 
                            uploaded_file.name,
                            model_map_transcribe_model[st.session_state["transcribe_model"]])
                        st.success('Översättning klar.')

                        st.balloons()

            
            # If audio has been translated, creates Word document with translation
            if st.session_state["translation"]:
                document = Document()
                document.add_paragraph(st.session_state.transcribed_en)

                document.save('text/' + uploaded_file.name + '_en.docx')

                with open("text/" + uploaded_file.name + "_en.docx", "rb") as template_file_en:
                    template_byte_en = template_file_en.read()

            # Creates a Word document with the transcribed text
            document = Document()
            document.add_paragraph(st.session_state.transcribed)

            document.save('text/' + uploaded_file.name + '.docx')

            with open("text/" + uploaded_file.name + ".docx", "rb") as template_file:
                template_byte = template_file.read()


            # Creates a grid of four columns for the different transcribed document download buttons
            col1, col2, col3, col4 = st.columns(4)
            
            # Text
            with col1:
                with open('text/' + uploaded_file.name + '.txt', "rb") as file_txt:
                    st.download_button(
                        label = ":flag-se: Ladda ned text",
                        data = file_txt,
                        file_name = uploaded_file.name + '.txt',
                        mime = 'text/plain',
                    )

            # Word
            with col2:
                st.download_button(
                    label = ":flag-se: Ladda ned word",
                    data = template_byte,
                    file_name = uploaded_file.name + '.docx',
                    mime = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                )

            # srt - subtitle
            with col3:
                with open('text/' + uploaded_file.name + '.srt', "rb") as file_srt:
                    st.download_button(
                        label = ":flag-se: Ladda ned srt",
                        data = file_srt,
                        file_name = uploaded_file.name + '.srt',
                        mime = 'text/plain',
                    )

            # Json
            with col4:
                with open('text/' + uploaded_file.name + '.json', "rb") as file_json:
                    st.download_button(
                        label = ":flag-se: Ladda ned json",
                        data = file_json,
                        file_name = uploaded_file.name + '.json',
                        mime = 'application/json',
                    )

            #If text is also translated it creates another row with four columns
            if st.session_state["translation"]:

                col5, col6, col7, col8 = st.columns(4)

                # Text
                with col5:
                    with open('text/' + uploaded_file.name + '_en.txt', "rb") as file_txt:
                        st.download_button(
                            label = ":flag-gb: Download text",
                            data = file_txt,
                            file_name = uploaded_file.name + '_en.txt',
                            mime = 'text/plain',
                        )

                # Word
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

        audio = st.audio_input("Spela in")

        # The rest of the code in tab2 works the same way as in tab1, so it's not going to be
        # commented.
        if audio:

            # Open the saved audio file and compute its hash
            current_file_hash = compute_file_hash(audio)

            # If the uploaded file hash is different from the one in session state, reset the state
            if "file_hash" not in st.session_state or st.session_state.file_hash != current_file_hash:
                st.session_state.file_hash = current_file_hash
                
                if "transcribed" in st.session_state:
                    del st.session_state.transcribed

            if "transcribed" not in st.session_state:

                audio_file = AudioSegment.from_file(audio)
                output_path = "audio/converted.mp3"
                audio_file.export(output_path, format="mp3", bitrate="16k")
                #print(f"Saved {output_path} as MP3")
                #chunk_paths.append(output_path)

                with st.spinner('Transkriberar. Det här kan ta ett litet tag beroende på hur lång inspelningen är...'):
                    st.session_state.transcribed = transcribe_with_whisper_stable("audio/converted.mp3", 
                        "local_recording.mp3",
                        model_map_transcribe_model[st.session_state["transcribe_model"]],
                        model_map_spoken_language[st.session_state["spoken_language"]]
                        )

                    st.success('Transkribering klar.')

                    st.balloons()

                if st.session_state["translation"]:
                    with st.spinner('Översätter. Det här kan ta ett litet tag beroende på hur lång inspelningen är...'):
                        st.session_state.transcribed_en = translate_with_whisper_stable("audio/converted.mp3", 
                            "local_recording.mp3",
                            model_map_transcribe_model[st.session_state["transcribe_model"]]
                            )
                        st.success('Översättning klar.')

                        st.balloons()

            if st.session_state["translation"]:
                document = Document()
                document.add_paragraph(st.session_state.transcribed_en)

                document.save('text/' + uploaded_file.name + '_en.docx')

                with open("text/" + uploaded_file.name + "_en.docx", "rb") as template_file_en:
                    template_byte_en = template_file_en.read()

            local_recording_name = "local_recording.mp3"
            document = Document()
            document.add_paragraph(st.session_state.transcribed)

            document.save('text/' + local_recording_name + '.docx')

            with open("text/local_recording.mp3.docx", "rb") as template_file:
                template_byte = template_file.read()

            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                with open('text/' + local_recording_name + '.txt', "rb") as file_txt:
                    st.download_button(
                        label = ":flag-se: Ladda ned text",
                        data = file_txt,
                        file_name = local_recording_name + '.txt',
                        mime = 'text/plain',
                    )

            with col2:
                st.download_button(
                    label = ":flag-se: Ladda ned word",
                    data = template_byte,
                    file_name = local_recording_name + '.docx',
                    mime = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                )

            with col3:
                with open('text/' + local_recording_name+ '.srt', "rb") as file_srt:
                    st.download_button(
                        label = ":flag-se: Ladda ned srt",
                        data = file_srt,
                        file_name = local_recording_name + '.srt',
                        mime = 'text/plain',
                    )

            with col4:
                with open('text/' + local_recording_name + '.json', "rb") as file_json:
                    st.download_button(
                        label = ":flag-se: Ladda ned json",
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



