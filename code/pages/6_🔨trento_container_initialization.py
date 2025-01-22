#!/usr/bin/python3

import time
import streamlit as st
import config as cfg
import helpers.start_support_container as ssc
import helpers.visual_funcs as vf
import helpers.layout_helpers as lh
import helpers.call_backs as hcb
import helpers.handle_support_file as hsf
from os import system, path
import helpers.tcsc_checks as tcsc_checks

cur_dir = path.dirname(path.realpath(__file__))
vf.local_css(f"{cur_dir}/style.css")

start_time = time.perf_counter()

if st.session_state.get("logged_in", None) :
    project = None
    project_support_files = None
    groups = ["all", "corosync", "sbd"]
    username = st.session_state.username
    user_dir = f"{cfg.Config.UPLOAD_DIR}/{username}"
    support_file_dir = f"{user_dir}/support_files"
    workspace = f"{user_dir}/scripts"
    if not path.isdir(workspace):
        system(f"mkdir -p {workspace}")

    st.title("Trento Initial Setup")
    col1, *_ = vf.create_columns(3, [0, 1, 1])
    col1.write("""On this page you initialize the Trento containers to prepare checks on your supportconfig files.""")
    col1.write('___')
    grid_parent = st.empty()

    col1, col2, col3 = st.columns([0.3, 0.1, 0.6])
    col3_frame = col3.columns(4)
    col3 = col3_frame[0]
    col4 = col3_frame[1]
    vf.make_big_vspace(1, col3)
    vf.make_big_vspace(1, col4)
    vf.make_big_vspace(1, col1)
    vf.make_big_vspace(1, col2)

    sradio_help = """Parse one/multiple supportconfig files or check historical data from 
        a recent project"""
    support_action_radio = col1.radio("Choose an option", ["__Create a new project__", "__Revisit historical check results__"],
        help=sradio_help, horizontal=True, index=0)
    if support_action_radio == "__Create a new project__":
        project = col3.text_input(
            "Project Name",
            help="""Enter an identifier for the Project, 
            e.g. the SR number""",
            on_change=hcb.clb_text_input,args=(col3, "Project must not be empty"),
        )
        cluster =  col2.checkbox(help="""Check this box if you want to compare multiple supportconfig files,
                         e.g. from a cluster""", label="Cluster")
    else:
        st.switch_page("pages/8_🔍trento_checks.py")

    vf.make_big_vspace(1, col1)
    vf.make_big_vspace(2, col3)
    col1.markdown("##### Select supportconfig file/s you want to execute Trento checks on")
    toggle_ph = col3.empty()
    # vf.make_big_vspace(1, col1)
    if project and support_action_radio == "__Create a new project__":
        support_files = hsf.get_support_config_files(support_file_dir)
        help =  """
        Only files starting with scc_ and suffix .txz are considered supportconfig files.
        """
        
        if not cluster:
            project_support_files = col1.selectbox("Supportconfig files", support_files,
                help=help )
        else:
            project_support_files = col1.multiselect("Supportconfig files", support_files,
                help=help )
        # if  support_files and support_files[0] == 0:
        if not support_files:
            col1.info("""You don't have any supportconfig files to check with trento.
                Please upload a supportconfig first.""")
            col1.page_link("pages/5_📂manage supportconfigs.py", label="Go to the Upload page",
                                   icon="📂")
            support_files = []

    if project and support_files:
        # with st.spinner(f"Investigating supportconfig files {support_files}"):
        vf.make_vspace(5, col1)
        col1 = st.columns([1])[0]

        if not cluster:
            project_support_files = [project_support_files]
        support_files_pathes = [f"{support_file_dir}/{x}" for x in project_support_files]
        if project_support_files:
            col_displ = col1
            show_info = toggle_ph.toggle("Display basic supportconfig information", False)
            basic_info = lh.get_basic_information(support_files_pathes)
            if show_info:
                col1.write(basic_info)
            vf.make_vspace(1, col1)
            arbitr_key  = list(basic_info.keys())[0]
            manufacturer = basic_info[arbitr_key]["hardware"]["Manufacturer"].strip()
            comps = ["Xen", "VMware", "KVM", "Microsoft Corporation", "Google", "Lenovo", "Amazon EC2"]
            index = comps.index(manufacturer) if manufacturer in comps else 0
            col1.radio(f"Manufacturer {manufacturer} detected", 
                comps, index=index,horizontal=True, help="Correct the manufacturer if it has been wrongly detected")

        col1_1, col1_2 = col1.columns([0.2,0.8])
        vf.make_big_vspace(1, col1)
        wanda_ret_code = 1
        env_check = tcsc_checks.check_environment(col1_1)
        if env_check:
            if col1.button("Initialize Containers", on_click=lh.trento_check_post, args=(support_files,)):
                with st.spinner("Waiting for container starts ..."):
                    col1.write("")
                    col1, col2, col3 = st.columns([0.5, 0.3, 0.2])
                    script_container = col1.container(border=True)
                    wanda_dict = {"project": project}
                    ssc.start_containers(workspace,script_container, support_files_pathes, wanda_dict)
                wanda_ret_code = tcsc_checks.check_project_status(script_container, project)

            vf.make_big_vspace(1, col1)
            col1_1, col1_2 = col1.columns([0.2,0.8])
            if wanda_ret_code == 0:
                df, support_file = hsf.load_support_file(username)
                projects = hsf.get_projects(username)
                if project not in projects:
                    hsf.initial_update_support_file(username, support_file, project_support_files, 
                        project, basic_info)
                col1_2.page_link("pages/8_🔍trento_checks.py", label=f"""Go to Trento Checks for the final analyzis
                    of project {project}""", icon="🔍")
            vf.make_big_vspace(1, col1)
        else:
            col1_1.warning("Please correct the environment issues first")
        if col1.button("Back to top", on_click=lh.trento_check_clean_up):
            pass
        
else:
    st.warning("you are not logged in, login first")
    st.switch_page("app.py")

end = time.perf_counter()
st.write(f'process_time: {round(end-start_time, 4)}')

# Manufacturer:  Amazon EC2, Xen, VMware, KVM, Microsoft Corporation, Google, Lenovo