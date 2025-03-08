import streamlit as st
import random
import time
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
