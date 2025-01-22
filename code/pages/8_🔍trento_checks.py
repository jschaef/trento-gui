import streamlit as st
import helpers.handle_support_file as hsf
import helpers.visual_funcs as vf
import helpers.tcsc_checks as tcsc_checks
import helpers.format_wanda_output as fwo
import config as cfg
from os import path, system

if st.session_state.get("logged_in", None):
    st.title("Trento Checks")
    cols = st.columns(2)
    col1 = cols[0]

    col1.write("""This page allows you to execute Trento checks on your projects.
             And/or shows historical data from a recent project""")
    col1.markdown("___")
    username = st.session_state.username
    df, _ = hsf.load_support_file(username)
    projects = hsf.get_projects(username)
    projects.sort()
    cols = st.columns([0.2, 0.4, 0.4])
    col1 = cols[0]
    colsb = st.columns([0.5, 0.5])
    col1b = colsb[0]
    if projects:
        project = col1.selectbox("select the project you want to execute the tests on", projects, key="project")    
        user_dir = f"{cfg.Config.UPLOAD_DIR}/{username}"
        workspace = f"{user_dir}/scripts"
        if not path.isdir(workspace):
            system(f"mkdir -p {workspace}")

        vf.make_vspace(3, col1)

        check_results = hsf.get_check_results(username, project)
        if len(check_results) > 1:
            if col1b.button(f"Show check results for {project}", key="run_historical_checks"):
                format_output = fwo.format_output(check_results, col1b)
        else: 
            if col1b.button(f"Run initial checks for {project}", key="run_checks"):
                col1b.info(f"""project {project} seems to be running the 
                    first time and needs to be processed. Be patient - 
                    it may take a while""")
                script_container = col1b.container(border=True)
                ret = tcsc_checks.run_checks(workspace, username, project, col1b)
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