import streamlit as st
import config as cfg
import user

def user_action():
    user_file = cfg.Config.USERS_FILE
    result, username = user.signup(user_file)
    return result, username

if "logged_in" not in st.session_state:
    selection, user = user_action()
    if selection:
        st.session_state.logged_in = True
        st.session_state.login_task = None
        st.session_state.username = user
        st.success("You have been logged in")
        st.switch_page("app.py")
else:
    st.warning("you are already logged in, logout first to signup again")
    


