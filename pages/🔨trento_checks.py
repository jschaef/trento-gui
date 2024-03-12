#!/usr/bin/python3

import streamlit as st
import config as cfg
import helpers.start_support_container as ssc
import helpers.visual_funcs as vf
import helpers.layout_helpers as lh
from os import system
import time

start_time = time.perf_counter()

if st.session_state.get("logged_in", None) :
    username = st.session_state.username
    workspace = f"{cfg.Config.UPLOAD_DIR}/{username}/scripts"
    host_group = ""
    system(f"mkdir -p {workspace}")

    st.title("Trento Checks")
    col1, *_ = vf.create_columns(3, [0, 1, 1])
    col1.write("This page is for Trento checks")
    col1.write("""Select the parameters for the checks you want to run. If you 
             want to compare multiple supportconfig files of a cluster, 
             you can use the hostgroup option.
             Else you can select a single supportconfig file to check (default).""")
    col1.write('___')
    grid_parent = st.empty()

    col1, col2 = st.columns([0.5, 0.6])
    col3 = col2.columns(4)[0]
    vf.make_big_vspace(3, col3)
    vf.make_big_vspace(1, col1)
    vf.make_big_vspace(1, col1)
    host_gr_bool = col1.toggle("Use hostgroup", False, help="Compare mulitple support config files of a cluster")
    if host_gr_bool:
        host_group = col3.text_input("Hostgroup Name",  help="Enter an identifier for the hostgroup")
    vf.make_big_vspace(1, col1)
    col1.markdown("##### Select supportconfig files you want to investigate")
    vf.make_big_vspace(1, col1)
    if host_gr_bool:
        support_files, col2_ph = lh.collect_support_files(col1)
        if support_files and support_files[0] == 0:
            col1.info("""You don't have any supportconfig files to check with trento.
                Please upload a supportconfig first.""")
            col1.page_link("pages/📂supportconfigs-upload.py", label="Go to the Upload page",
                                   icon="📂")
            support_files = []
    else:
        col_for_list = col1.columns([1, 1])[0]
        support_files_bname = lh.get_support_files(col_for_list)
        if support_files_bname:
            support_files = [f"{cfg.Config.UPLOAD_DIR}/{username}/support_files/{x}" for x in [support_files_bname]]  
        else:
            col1.info("""You don't have any supportconfig files to check with trento.
                Please upload a supportconfig first.""")
            col1.page_link("pages/📂supportconfigs-upload.py", label="Go to the Upload page",
                                   icon="📂")
            
            support_files = []
    col1, col2 = st.columns([0.3, 0.7])


    if support_files:
        # with st.spinner(f"Investigating supportconfig files {support_files}"):
        vf.make_vspace(5, col1)
        col_displ = col2_ph if host_gr_bool else col1
        show_info = col_displ.toggle("Display basic supportconfig information", False)
        basic_info = lh.get_basic_information(support_files)
        if show_info:
            col1.write(basic_info)
        groups = ["all", "corosync", "sbd"]
        vf.make_vspace(1, col1)
        col1_1, col1_2 = col1.columns(2)
        checks = col1_1.selectbox("Select which Trento checks you want to execute", groups)
        vf.make_vspace(1, col1)
        if col1.button("Run Trento Checks", on_click=lh.trento_check_post, args=(support_files,)):
            if host_gr_bool and not host_group:
                col1.warning("Please enter a hostgroup name")
                lh.trento_check_clean_up()
            else:
                with st.spinner("Waiting for Trento checks to complete..."):
                    col1.write("")
                    col1, col2 = st.columns([0.7, 0.3])
                    script_container = col1.container(height=300, border=True)
                    ret_code = ssc.test_cmd(workspace,script_container)
                    vf.make_big_vspace(3, col1)
                    col1_1, col1_2 = col1.columns(2)
                    col1_1.write("""Please cleanup the workspace after you are done with the checks""")
                    if col1_2.button("Cleanup", help="Delete the supportconfig containers"):
                        pass
                    
                if col1.button("Back to top", on_click=lh.trento_check_clean_up):
                    pass
else:
    st.warning("you are not logged in, login first")
    st.switch_page("app.py")

end = time.perf_counter()
st.write(f'process_time: {round(end-start_time, 4)}')