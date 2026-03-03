import streamlit as st
import pyrebase
st.set_page_config(page_title="Portofolio Tracker",layout="wide")

firebaseConfig = dict(st.secrets["firebase"])

firebase= pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()

if "logged_in" not in st.session_state:
    st.session_state.logged_in= False
def login_screen():
    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        with st.form("login_form"):
            st.title("Welcome",)

            email = st.text_input("Username")
            password = st.text_input("Password", type="password")

            submit_button = st.form_submit_button("Submit",width="stretch")

            if submit_button:
                try:
                    user= auth.sign_in_with_email_and_password(email,password)

                    st.session_state.logged_in=True
                    st.session_state.user_email=email
                    st.rerun()
                    st.success("Log in successful.")
                except Exception as e:
                    st.error("Email or password is wrong.")


if not st.session_state.logged_in and not st.user.is_logged_in:
    login_screen()
    col1,col2,col3= st.columns([1,1,1])
    with col2:
        st.button("Log in with Google", on_click=st.login, use_container_width=True)
else:
    display_name = st.session_state.get("user_email") or st.user.name
    st.header(f"Welcome, {display_name}!")
    if st.button("Log out"):
        st.session_state.logged_in = False
        if st.user.is_logged_in:
            st.logout()
        st.rerun()
