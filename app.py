## Invoice Extracter

from dotenv import load_dotenv

load_dotenv() ## load all environment variables from .env

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

## configuring API key

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## function to load Gemini Pro vision model and get response

def get_gemini_response(input,image,prompt):
    ## loading the gemini model
    model=genai.GenerativeModel("gemini-1.5-flash")#'gemini-pro-vision')
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type, # Get the mime type of the uploaded file
                "data": bytes_data,
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


## initializing our streamlit app

st.set_page_config(page_title="Invoice Extractor")

st.header("Gemini Application")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])
image=""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit=st.button("Tell me about the invoice")

input_prompt="""
You are an expert in understanding invoices. You will
recieve input images as invoices and you will have to
answer questions based in the input image.
"""

## If submit button is clicked

if submit:
    image_data=input_image_setup(uploaded_file)
    #response=get_gemini_response(input_prompt,image_data,input) gpt ดันบอกว่าสลับไม่ได้
    response=get_gemini_response(input,image_data,input_prompt) 

    st.subheader("The Response is")
    st.write(response)