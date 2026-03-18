from auth import *

st.set_page_config(page_title="Portofolio Tracker", layout="wide")


if "logged_in" not in st.session_state:
    st.session_state.logged_in= False
if "user_email" not in st.session_state:
    st.session_state.user_email= None
if "id_token" not in st.session_state:
    st.session_state.id_token=None



is_firebase_logged = st.session_state.logged_in
is_google_logged= st.user.is_logged_in

pages = [
        st.Page("pages/1_Home.py", title="Home"),
        st.Page("pages/2_Portfolio.py", title="Portfolio"),
        st.Page("pages/3_Market.py", title="Market"),
        st.Page("pages/4_Transactions.py", title="Transactions"),
        st.Page("pages/5_Settings.py", title="Settings"),
    ]


if is_firebase_logged or is_google_logged:
    pg= st.navigation(pages)
    pg.run()
else:
    login_page= [st.Page(login_screen,title="Log in")]
    pg = st.navigation(login_page,position="hidden")
    pg.run()