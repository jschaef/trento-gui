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

    col1.write(
        """This page allows you to execute Trento checks on your projects.
             And/or shows historical data from a recent project"""
    )
    col1.markdown("___")
    username = st.session_state.username
    df, _ = hsf.load_support_file(username)
    projects = hsf.get_projects(username)
    projects.sort()
    cols = st.columns([0.15, 0.15, 0.1, 0.1, 0.2])
    col1 = cols[0]
    col2 = cols[1]
    col3 = cols[2]
    col4 = cols[3]
    colsb = st.columns([0.5, 0.5])
    col1b = colsb[0]
    checks_run = 0
    message_types = ["all", "passing", "critical", "warning"]

    if projects:
        action = col1.radio(
            "Select the action you want to perform",
            ["Run checks", "Manage old projects"],
            index=0,
            key="action",
            horizontal=True,
        )
        if action == "Run checks":
            project = col2.selectbox(
                "select the project you want to execute the tests on",
                projects,
                key="project",
                help="Select project",
            )
            user_dir = f"{cfg.Config.UPLOAD_DIR}/{username}"
            workspace = f"{user_dir}/scripts"
            if not path.isdir(workspace):
                system(f"mkdir -p {workspace}")

            vf.make_vspace(3, col1)
            vf.make_vspace(3, col2)

            container_placeholder = col1b.empty()
            result_container = container_placeholder.container(border=True)
            check_results = hsf.get_check_results(username, project)
            if len(check_results) > 1:
                topic = col3.selectbox(
                    "select the topic you want to filter",
                    [
                        "all",
                        "Corosync",
                        "SBD",
                        "Pacemaker",
                        "OS and package versions",
                        "saptune",
                        "Azure Fence Agent",
                        "Filesystems",
                        "Sapservices",
                        "SAP HANA System Replication Resource Agent ocf:suse:SAPHana",
                    ],
                    key="topic",
                )
                message_type = col4.selectbox(
                    "select the message type you want to filter",
                    message_types,
                    key="message_type",
                    help=f"Select message type: {', '.join(message_types)}",
                )
                if col1.button(
                    f"Show check results for {project}", key="run_historical_checks"
                ):
                    vf.make_vspace(3, col1b)
                    format_output = fwo.format_output(
                        check_results, result_container, topic, message_type
                    )
                checks_run = 1

            else:
                if col1.button(f"Run initial checks for {project}", key="run_checks"):
                    col1b.info(
                        f"""project {project} seems to be running the 
                        first time and needs to be processed. Be patient - 
                        it may take a while"""
                    )
                    ret = tcsc_checks.run_checks(
                        workspace, username, project, result_container
                    )
                    checks_run = 1
            if checks_run:
                vf.make_vspace(3, col1)
                if col1b.button("Back to top", on_click=container_placeholder.empty):
                    pass
                if col2.button("Clear screen", key="clear_screen"):
                    container_placeholder.empty()

        elif action == "Manage old projects":
            if projects:
                project = col2.selectbox(
                    "select the project you want to delete", projects, key="project"
                )
                if col1.button(f"Delete project {project}", key="delete_project"):
                    hsf.delete_project_record(username, project)
                    st.rerun()
            else:
                col1.write("No projects found, please create a project first")
                col1.page_link(
                    "pages/6_🔨trento_project_setup.py",
                    label="Go to the Trento Initialization page",
                    icon="🔨",
                )
    else:
        col1.write("No projects found, please create a project first")
        col1.page_link(
            "pages/6_🔨trento_project_setup.py",
            label="Go to the Trento Initialization page",
            icon="🔨",
        )

else:
    st.warning("you are not logged in, login first")
    st.switch_page("app.py")
