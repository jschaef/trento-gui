import streamlit as st

st.session_state.pop("logged_in", None)
st.session_state.pop("login_task", None)
st.session_state.pop("_login_task", None)
st.session_state.pop("user_role", None)
st.session_state.pop("username", None)
st.info("You have been logged out")