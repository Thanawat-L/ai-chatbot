import streamlit as st

st.title("🎈 My chatbot app")

# Step 1: Initialize session state for storing chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Initialize with an empty list

# Step 2: Display the user input
user_input = st.text_input("You: ", placeholder="Type your message here...")
st.write("User input: ", user_input)
if user_input:
    # Step 3: Add the user input to chat history
    st.session_state.chat_history.append(user_input)

# Step 4: Display all messages using st.write
for message in st.session_state.chat_history:
    st.write(message)

'--------------------------------------------------------------------------------------'

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("Type your message here...")
if user_input:
    st.session_state.chat_history.append(user_input)

    message = st.chat_message("assistant")
    message.write(f"User has sent the following prompt: {user_input}")

'--------------------------------------------------------------------------------------'

import streamlit as st
import google.generativeai as genai

# Title and Subheader
st.title("My chatbot app")
st.subheader("Conversation")

# Input for API Key
gemini_api_key = st.text_input("Gemini API Key: ", placeholder="Type your API Key here...", type="password")

# Configuring API Key
if gemini_api_key:
    try:
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-pro")
        st.success("Gemini API Key successfully configured.")
    except Exception as e:
        st.error(f"Error configuring Gemini API Key: {e}")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for role, message in st.session_state.chat_history:
    st.chat_message(role).markdown(message)

# Capture user input and generate AI response
if user_input := st.chat_input("Type your message here..."):
    # Add user input to chat history
    st.session_state.chat_history.append(("user", user_input))
    st.chat_message("user").markdown(user_input)

    # Generate response using Gemini API
    if model:
        try:
            response = model.generate_content(user_input)
            bot_response = response.text

            # Add AI response to chat history
            st.session_state.chat_history.append(("assistant", bot_response))
            st.chat_message("assistant").markdown(bot_response)

        except Exception as e:
            st.error(f"Error generating AI response: {e}")