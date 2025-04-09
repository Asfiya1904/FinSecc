
import streamlit as st
import openai
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="FinSec", layout="wide", page_icon="🛡️")

st.sidebar.image("finsec_logo.png", use_column_width=True)
st.sidebar.title("FinSec Navigation")

menu = st.sidebar.radio("Go to", ["Login", "Dashboard", "Chatbot", "Settings", "Privacy Policy", "Logout"])

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if menu == "Login":
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if email and password:
            st.session_state.logged_in = True
            st.success("Logged in successfully")
            st.experimental_rerun()
        else:
            st.error("Enter both fields")

if menu == "Dashboard" and st.session_state.logged_in:
    st.title("📊 FinSec Dashboard")
    st.write("Upload and analyze your transactions here.")

if menu == "Chatbot" and st.session_state.logged_in:
    st.title("🤖 AI Assistant")
    user_input = st.text_input("Ask FinSec AI")
    if user_input:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        try:
            with st.spinner("Thinking..."):
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant for FinSec, a financial fraud detection platform."},
                        {"role": "user", "content": user_input}
                    ]
                )
                answer = response["choices"][0]["message"]["content"]
                st.success(answer)
        except Exception as e:
            st.error(f"Failed to connect to OpenAI API: {e}")

if menu == "Settings" and st.session_state.logged_in:
    st.title("Settings")
    st.text_input("Webhook URL")
    st.toggle("Enable Email Alerts", value=True)

if menu == "Privacy Policy":
    st.title("📜 Privacy Policy")
    with open("privacy_policy.md") as f:
        st.markdown(f.read())
    st.markdown("""""" + footer_html + """"", unsafe_allow_html=True)

if menu == "Logout" and st.session_state.logged_in:
    if st.button("Click here to Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.success("You have been logged out.")
        st.experimental_rerun()
