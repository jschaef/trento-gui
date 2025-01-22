import streamlit as st
import helpers.handle_support_file as hsf
import helpers.visual_funcs as vf
import helpers.tcsc_checks as tcsc_checks
import config as cfg
from os import path, system

if st.session_state.get("logged_in", None):
    st.title("Trento Checks")
    cols = st.columns(2)
    col1 = cols[0]

    col1.write("""This page allows you to execute Trento checks on your projects.
             And/or show historical data from a recent project""")
    col1.markdown("___")
    username = st.session_state.username
    df, _ = hsf.load_support_file(username)
    projects = hsf.get_projects(username)
    cols = st.columns([0.2, 0.4, 0.4])
    col1 = cols[0]
    if projects:
        project = col1.selectbox("__select the project you want to execute the tests on__", projects)
        user_dir = f"{cfg.Config.UPLOAD_DIR}/{username}"
        workspace = f"{user_dir}/scripts"
        if not path.isdir(workspace):
            system(f"mkdir -p {workspace}")

        vf.make_big_vspace(1, col1)

        if col1.button("Run checks"):
            cols = st.columns([0.5, 0.5])
            col1 = cols[0]
            script_container = col1.container(border=True)
            ret = tcsc_checks.run_checks(workspace, username, project, col1)
            col1.write(ret)
    else:
        col1.write("No projects found, please create a project first")
        col1.page_link(
            "pages/6_🔨trento_container_initialization.py",
            label="Go to the Trento Initialization page",
            icon="🔨",
        )   

else:
    st.warning("you are not logged in, login first")
    st.switch_page("app.py")