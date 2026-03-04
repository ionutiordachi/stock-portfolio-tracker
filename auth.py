import streamlit as st
import requests

FIREBASE_API_KEY = st.secrets["firebase"]["apiKey"]

FIREBASE_SIGN_IN_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
FIREBASE_SIGN_UP_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_API_KEY}"
def firebase_register(email:str, password:str)->dict:
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    response = requests.post(FIREBASE_SIGN_UP_URL,json=payload)
    data=response.json()

    if "error" in data:
        raise ValueError(data["error"]["message"])
    return data

def firebase_login(email: str, password: str) -> dict:
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    response = requests.post(FIREBASE_SIGN_IN_URL, json=payload)
    data = response.json()

    if "error" in data:
        raise ValueError(data["error"]["message"])
    return data
def parse_firebase_error(error_message:str)->str:
    errors = {
            "INVALID_PASSWORD":"Wrong password",
            "INVALID_LOGIN_CREDENTIALS": "Invalid email or password",
            "EMAIL_NOT_FOUND":"No account found with this email.",
            "USER_DISABLED":"Account has been disabled.",
            "TOO_MANY_ATTEMPTS_TRY_LATER":"Too many attempts. Try again later.",
            "MISSING PASSWORD":"Password cannot pe empty",
            "INVALID_EMAIL":"Invalid email format.",
    }
    for code, message in errors.items():
        if code in error_message:
            return message
    return f"Eroare necunoscuta: {error_message}"


def login_screen():
    col1,col2,col3 = st.columns([1,1,1])

    with col2:
        st.title("Welcome")

        tab1,tab2 = st.tabs(["Log in", "Register"])
        with tab1:
            with st.form("login_form"):
                email= st.text_input("Email")
                password = st.text_input("Parola",type="password")
                submit = st.form_submit_button("Log in", use_container_width=True)

                if submit:
                    if not email or not password:
                        st.warning("Completeaza email si parola!")
                    else:
                        try:
                            user_data= firebase_login(email,password)

                            st.session_state.logged_in= True
                            st.session_state.user_email = user_data["email"]
                            st.session_state.id_token = user_data["idToken"]

                            st.rerun()

                        except ValueError as e:
                            st.error(parse_firebase_error(str(e)))
        with tab2:
            with st.form("register_form"):
                reg_email=st.text_input("Email")
                reg_password1 = st.text_input("Password", type="password")
                reg_password2 = st.text_input("Confirm Password", type="password")
                reg_submit= st.form_submit_button("Create account", use_container_width=True)

                if reg_submit:
                    if not reg_email or not reg_password1 or not reg_password2:
                        st.warning("Fill in all the fields!")
                    elif reg_password1 != reg_password2:
                        st.warning("The passwords don't match")
                    else:
                        try:
                            user_data = firebase_register(reg_email,reg_password1)

                            st.session_state.logged_in=True
                            st.session_state.user_email=user_data["email"]
                            st.session_state.id_token=user_data["idToken"]

                            st.rerun()
                        except ValueError as e:
                            st.error(parse_firebase_error(str(e)))

        st.button(
            "Continua cu Google",
            on_click=st.login,
            use_container_width=True
            )


