import streamlit as st
from menu import menu

st.set_page_config(
    page_title="Trento Supportconfig Analyzer",
    layout='wide',
    #page_icon="wiki_pictures/kisspng-penguin-download-ico-icon-penguin-5a702cc04e5fc1.8432243315173009283211.png",
    #page_icon="🐧",
    page_icon="🔍",
)

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
    col1.write("Choose your action from the sidebar menu.")


menu() # Render the dynamic menu!