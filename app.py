import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

st.set_page_config(page_title="Portofolio Tracker",layout="wide")

def login_screen():
    with st.form("login_form"):
        col1, col2, col3= st.columns([1,1,1])

        with col2:
            st.title("Welcome",)

            email = st.text_input("Username")
            password = st.text_input("Password", type="password")

            submit_button = st.form_submit_button("Submit",width="stretch")
        if submit_button:
            st.write(f"The system is attempting to log in for: {email}")


if not st.user.is_logged_in:
    login_screen()
    col1,col2,col3= st.columns([1,2,1])
    with col2:
        st.button("Log in with Google", on_click=st.login, use_container_width=True)
else:
    st.header(f"Welcome, {st.user.name}!")
    st.button("Log out", on_click=st.logout)