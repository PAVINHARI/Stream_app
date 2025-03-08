import streamlit as st
from huggingface_hub import InferenceClient

# Initialize Hugging Face API client
client = InferenceClient(model="HuggingFaceH4/zephyr-7b-beta")  # Model specified here

# Function to get chat response
def get_chat_response(user_input):
    messages = [{"role": "user", "content": user_input}]
    
    # Make a request to Hugging Face model
    response = client.post(json={"inputs": messages, "parameters": {"temperature": 0.7, "max_new_tokens": 1024, "top_p": 0.7}})
    
    return response  # Directly returning text response

# Streamlit UI
st.title("🤖 AI Chatbot")
st.write("Chat with an AI-powered assistant!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if user_input := st.chat_input("Enter your message..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get and display AI response
    with st.chat_message("assistant"):
        response = get_chat_response(user_input)
        st.markdown(response)

    # Add AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
