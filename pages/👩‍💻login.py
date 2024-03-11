import streamlit as st
import config as cfg
import user

def user_action():
    cols = st.columns(2)
    col1, col2 = cols

    user_file = cfg.Config.USERS_FILE
    result, username = user.login(user_file, col1)
    return result, username

if "logged_in" not in st.session_state:
    selection, username = user_action()
    if selection == "logged_in":
        st.session_state.logged_in = True
        st.session_state.login_task = None
        st.session_state.role = username
        st.success("You have been logged in")
        st.switch_page("app.py")
    elif selection == "user_exists":
        st.warning("user already exists, login instead or signup with a different username")
    elif selection == "user_not_exists":
        st.warning("user does not exist, signup instead or check your username and password")
else:
    st.warning("you are already logged in, logout first to login again")
