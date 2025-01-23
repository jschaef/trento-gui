import streamlit as st
import config as cfg
import user
import helpers.handle_users as user_mgmt
import helpers.layout_helpers as lh
from datetime import datetime

def user_action():
    cols = st.columns(2)
    col1, *_ = cols

    user_file = cfg.Config.USERS_FILE
    result, username = user.login(user_file, col1)
    return result, username

if "logged_in" not in st.session_state:
    selection, username = user_action()
    if selection == "logged_in":
        user_role = user.get_user_role(cfg.Config.USERS_FILE, username)
        user_mgmt.add_record(username, datetime.now(), True)
        st.session_state.user_role = user_role
        st.session_state.logged_in = True
        st.session_state.login_task = None
        st.session_state.username = username
        st.success("You have been logged in")
        st.switch_page("app.py")
    elif selection == "user_password_wrong":
        st.warning("wrong password")
        user_mgmt.add_record(username, datetime.now(), False)
    elif selection == "user_not_exists":
        st.warning("user does not exist, signup instead or check your username and password")
        user_mgmt.add_record(username, datetime.now(), False)
else:
    st.warning("you are already logged in, logout first to login again")

lh.display_admin_link()