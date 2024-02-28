import os
import streamlit as st
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv


load_dotenv()

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load GEMINI PRO model and get response
model = genai.GenerativeModel("gemini-pro")

# Define a function to map roles to Streamlit chat roles
def role_to_streamlit(role):
    if role == "model":
        return "assistant"
    else:
        return role

# Function to transcribe audio file to text
def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()

    # Convert the uploaded file into an audio source
    audio_source = sr.AudioFile(audio_file)

    with audio_source as source:
        audio_data = recognizer.record(source, duration=None)  # Capture entire audio

    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Sorry, I could not understand the audio."

# Function to convert text to speech using pyttsx3
def speak_text(text):
    # Initialize pyttsx3 engine
    engine = pyttsx3.init()

    # Set the speed rate of speech
    engine.setProperty('rate', 150)  # Adjust the speed as needed

    # Speak the response for a short period of time
    engine.say(text[:500])  # Read only the first 500 characters

    # Run and wait for the speech to finish
    engine.runAndWait()

# Check if chat history exists in session state, if not, initialize it
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# Display chat history
if hasattr(st.session_state, "chat") and st.session_state.chat.history:
    if not hasattr(st.session_state, "chat_displayed") or not st.session_state.chat_displayed:
        for message in st.session_state.chat.history:
            with st.chat_message(role_to_streamlit(message.role)):
                st.markdown(message.parts[0].text)
        st.session_state.chat_displayed = True

st.header("WELCOME TO MEDIBOT!!")

# Accept user input: text or audio file
user_input = st.radio("Choose input method:", ("Text", "Audio"))

if user_input == "Audio":
    uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"])
    if uploaded_file:
        # Transcribe entire audio to text
        audio_text = transcribe_audio(uploaded_file)

        # Display transcribed text
        if audio_text:
            st.info("Transcribed Audio:")
            st.write(audio_text)

            # Get response from the model using transcribed text as input
            response = st.session_state.chat.send_message(audio_text)

            # Display response as text
            with st.chat_message("assistant"):
                # Split response into bullet points
                response_points = response.text.split('\n')
                response_text = "\n".join([f"- {point}" for point in response_points])
                st.markdown(response_text)

                # Speak the response
                speak_text(response.text)
        else:
            st.error("Failed to transcribe audio.")

else:
    text_input = st.text_input("Enter your message:")
    if st.button("Send"):
        if text_input:
            # Get response from the model using text input
            response = st.session_state.chat.send_message(text_input)

            # Display response as text
            with st.chat_message("assistant"):
                # Split response into bullet points
                response_points = response.text.split('\n')
                response_text = "\n".join([f"- {point}" for point in response_points])
                st.markdown(response_text)

                # Speak the response
                speak_text(response.text)
        else:
            st.warning("Please enter a message before sending.")
