import streamlit as st
import random
import time
import base64
from huggingface_hub import InferenceClient  # Correct client import

# Cache the Hugging Face API client
@st.cache_resource
def get_client():
    return InferenceClient(api_key="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")

# Function to get chat response
def get_chat_response(prompt):
    client = get_client()  # Get cached client
    result = ""

    messages = [{"role": "user", "content": prompt}]
    
    stream = client.chat_completions.create(
        model="HuggingFaceH4/zephyr-7b-beta",
        messages=messages,
        temperature=0.7,
        max_tokens=1024,
        top_p=0.7,
        stream=True
    )

    for chunk in stream:
        result += chunk.choices[0].delta.content

    return result

# Function to add background image to main chat
def add_bg_from_local(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .ScrollToBottomContainer {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Function to add background image to sidebar
def add_bg_to_sidebar(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        [data-testid="stSidebar"] > div:first-child {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set background images
main_bg_path = 'imagefiles/pexels-padrinan-255379.jpg'
sidebar_bg_path = 'imagefiles/pill-tablet-pharmacy-medicine.jpg'
add_bg_from_local(main_bg_path)
add_bg_to_sidebar(sidebar_bg_path)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Enter your query"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get assistant response
    response = get_chat_response(prompt)
    
    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)

    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response})
