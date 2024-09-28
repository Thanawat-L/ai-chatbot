import streamlit as st
import google.generativeai as genai
import time

st.title(":medical_symbol: My GenAI Pharmacist chatbot")
gemini_api_key = st.text_input("Gemini API Key: ", placeholder="Type your API Key here...", type="password")

if "greeted" not in st.session_state:
    st.session_state.greeted = False 
if "success_state" not in st.session_state:
    st.session_state.success_state = False 

if gemini_api_key:
    try:
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-pro")
        if not st.session_state.success_state:
            success_placeholder = st.empty()
            success_placeholder.success("Gemini API Key successfully configured.")
            time.sleep(3)
            success_placeholder.empty()
            st.session_state.success_state = True
    except Exception as e:
        st.error(f"Error configuring Gemini API Key: {e}")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for role, message in st.session_state.chat_history:
        st.chat_message(role).markdown(message)

    if not st.session_state.greeted:
        greeting_prompt = "Greet the user as a friendly and knowledgeable pharmacist. \
                        Introduce yourself (your are GenAI Pharmacist) and let the user know you're here to assist with \
                        any questions they may have about their medications or health conditions. \
                        Make sure to create a welcoming and supportive environment, \
                        ensuring the user feels comfortable asking about their concerns."

        try:
            response = model.generate_content(greeting_prompt)
            bot_response = response.text
            st.session_state.chat_history.append(("assistant", bot_response))
            st.chat_message("assistant").markdown(bot_response)
            st.session_state.greeted = True
        except Exception as e:
            st.error(f"Error generating AI greeting: {e}")

    if user_input := st.chat_input("Type your message here..."):
        st.session_state.chat_history.append(("user", user_input))
        st.chat_message("user").markdown(user_input)

        try:
            prompt = "You are a knowledgeable and friendly pharmacist. \
            Your role is to assist users by providing clear, concise, \
            and helpful information about medications and their proper use. \
            Here is the chat history:\n"

            for role, message in st.session_state.chat_history:
                prompt += f"{role}: {message}\n"

            prompt += f"User: {user_input}\n"

            prompt += "Please respond based on the information above, including dosage instructions, \
                        potential side effects, precautions, and advice on how to take the medication. \
                        Ensure your responses are accurate and adhere to the highest pharmaceutical standards. \
                        Inform users when they should seek further medical attention or consult a healthcare provider."

            response = model.generate_content(prompt)
            bot_response = response.text

            st.session_state.chat_history.append(("assistant", bot_response))
            st.chat_message("assistant").markdown(bot_response)

        except Exception as e:
            st.error(f"Error generating AI response: {e}")