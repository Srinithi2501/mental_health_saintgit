from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
import base64

# Load environment variables
load_dotenv()

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# Function to load Google Gemini Pro Vision API And get response
def get_gemini_vision_response(input_prompt, image_data):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_prompt, image_data[0]])
    return response.text


def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


def get_gemini_text_response(question):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(question)
    return response.text


def main():
    # Set Streamlit page configuration
    st.set_page_config(page_title="Report Explainer")

    # Sidebar for image uploader
    st.sidebar.header("Image Uploader")
    uploaded_file = st.sidebar.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Great! I will analyze this image", use_column_width=True)

    # Header for Peripheral Disease Detector
    st.header("Medibot - Report Explainer")
    input_prompt = """
    You are an expert in text detection of medical reports from images uploaded. You should 
    interpret each and every word written in the image, no matter how minute or small it is.
    """

    submit_image = st.button("Interpret Image")

    # If submit button for image is clicked
    if submit_image:
        if uploaded_file is not None:
            image_data = input_image_setup(uploaded_file)
            response = get_gemini_vision_response(input_prompt, image_data)
            st.subheader("The Image Interpretation Response is")
            st.write(response)
        else:
            st.error("Please upload an image first")

    # Question tab for asking questions
    st.header("Ask Questions")
    user_question = st.text_input("Ask a Question")

    submit_question = st.button("Submit Question")

    # If submit button for question is clicked
    if submit_question:
        if user_question:
            response = get_gemini_text_response(user_question)
            st.subheader("The Question Response is")
            st.write(response)


# Run the main function
if _name_ == "_main_":
    main()
