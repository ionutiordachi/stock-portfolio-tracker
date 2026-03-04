from auth import *

st.set_page_config(page_title="Portofolio Tracker", layout="wide")


if "logged_in" not in st.session_state:
    st.session_state.logged_in= False
if "user_email" not in st.session_state:
    st.session_state.user_email= None
if "id_token" not in st.session_state:
    st.session_state.id_token=None
def main_app():
    if st.user.is_logged_in:
        display_name=st.user.name or st.user.email
    else:
        display_name = st.session_state.user_email

    col1,col2= st.columns([5,1])
    with col1:
        st.header(f"Bun venit, {display_name}")
    with col2:
        if st.button("Log out", use_container_width= True):

            st.session_state.logged_in = False
            st.session_state.user_email=None
            st.session_state.id_token=None

            if st.user.is_logged_in:
                st.logout()
            else:
                st.rerun()
    st.divider()
    st.write("Portofolio Tracker - continut principal")

is_firebase_logged = st.session_state.logged_in
is_google_logged= st.user.is_logged_in

if is_firebase_logged or is_google_logged:
    main_app()
else:
    login_screen()
