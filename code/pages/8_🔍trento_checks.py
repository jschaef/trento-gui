import streamlit as st

if st.session_state.get("logged_in", None):
    st.write("This is a test page")
else:
    st.warning("you are not logged in, login first")
    st.switch_page("app.py")