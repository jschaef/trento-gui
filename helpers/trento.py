#!/usr/bin/python3
import streamlit as st
import config as cfg
import helpers.layout_helpers as lh

def support_file_picker(col: st.columns):
        username = st.session_state.username
        upload_dir = f"{cfg.Config.UPLOAD_DIR}/{username}/support_files"
        col.write('')
        selection = lh.get_support_files(upload_dir, col=col, key='support_files')  
        return selection
