import streamlit as st
from os import path
from menu import menu


st.set_page_config(
    page_title="Trento Supportconfig Analyzer",
    layout='wide',
    page_icon="🔍",
)

def local_css(file_name: str):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

cur_dir = path.dirname(path.realpath(__file__))
local_css(f"{cur_dir}/style.css")

# Initialize st.session_state.role to None
if "login_task" not in st.session_state:
    st.session_state.login_task = None

# Retrieve the action from Session State to initialize the widget
st.session_state._login_task = st.session_state.login_task

def set_login():
    # Callback function to save the role selection to Session State
    st.session_state.login_task = st.session_state._login_task

# Selectbox to choose task
cols = st.columns(4)
col1, col2, *_  = cols

if not st.session_state.get("logged_in", None) :
    col1.selectbox(
        "Select your action:",
        ["login", "signup", "forgot-password"],
        key="_login_task",
        on_change=set_login,
    )
    #st.button("Submit", on_click=set_login)
else:
    col1.write("#### You are logged in now.")
    col1.write("Choose your action from the sidebar menu.")
    col1.write("""You probably wanto to upload one or multiple supportconfig 
               files or check existing projects with Trento.""")



menu() # Render the dynamic menu!