import os
import streamlit as st
import config as cfg
import helpers.tar_file_reader as tfr
from typing import Optional

def get_support_files(col: Optional[st.delta_generator.DeltaGenerator]=None, key: Optional[str]=None):
    username = st.session_state.username
    base_dir = os.getcwd()
    upload_dir = f"{base_dir}/{cfg.Config.UPLOAD_DIR}/{username}/support_files"
    if not os.path.isdir(upload_dir):
        os.makedirs(upload_dir)
    support_files = [x for x in os.listdir(upload_dir) \
        if os.path.isfile(f'{upload_dir}/{x}') ]

    if support_files:
        if not col:
            col1, col2, col3 = st.columns([2,1, 1])
            col1.write(''), col3.write('')
            selection = col2.selectbox('support_files', support_files, key=key,
                on_change=trento_check_clean_up)
        else:
            selection = col.selectbox('support_files', support_files, key=key)
    else:
        selection = None
    return selection

def collect_support_files(col: st.columns,) -> list:
    cols_cont = col.columns([1, 1])
    col1 = cols_cont[0]
    col2 = cols_cont[1]
    check_field = []
    username = st.session_state.username
    base_dir = os.getcwd()
    upload_dir = f"{cfg.Config.UPLOAD_DIR}/{username}/support_files"
    col1.write('')
    col2.write('')
    support_files = [x for x in os.listdir(upload_dir) \
        if os.path.isfile(f'{upload_dir}/{x}') ]
    if not support_files:
        return [0], col2
    for file in support_files:
        key = f"sel_{support_files.index(file)}_{file}"
        chked = col1.checkbox(
            support_files[support_files.index(file)],
            key=key,
            value=False,
            args=([file]),
        )
        if chked:
            check_field.append(support_files[support_files.index(file)])

    col2_ph = col2.empty()
    path_field = [f"{base_dir}/{upload_dir}/{x}" for x in check_field]
    return path_field, col2_ph

def get_basic_information(path_field: list) -> dict:
    return_dict = {}
    file_info_dict = st.session_state.get("file_info_dict", {})
    cmp_dict = file_info_dict.copy()
    for file in path_field:
        base_file = os.path.basename(file)
        if base_file not in file_info_dict.keys():
            with st.spinner(f"Reading {file}..."):
                file_info_dict[base_file] = tfr.get_basic_information(file)
        return_dict[base_file] = file_info_dict[base_file]
    if cmp_dict != file_info_dict:
        st.session_state.file_info_dict = file_info_dict
    
    return return_dict
        
def trento_check_post(support_files):
    st.session_state.trento_check = support_files 

def trento_check_clean_up():
    st.session_state.pop("trento_check", None)
