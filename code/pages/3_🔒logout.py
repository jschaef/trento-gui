import streamlit as st

col1, *_ = st.columns([0.2,0.8])
st.session_state.pop("logged_in", None)
st.session_state.pop("login_task", None)
st.session_state.pop("_login_task", None)
st.session_state.pop("user_role", None)
st.session_state.pop("username", None)
col1.info("You have been logged out")