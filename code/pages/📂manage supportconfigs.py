import upload_mgt
from os import path
import streamlit as st

if st.session_state.get("logged_in", None) :
    username = st.session_state.username
    st.write(f"Welcome {username}")
    cur_dir = path.dirname(path.realpath(__file__))
    upload_dir = f"{path.dirname(cur_dir)}/upload/{username}/support_files"
    upload_mgt.file_mngmt(upload_dir)

else:
    st.switch_page("pages/👩‍💻login.py")