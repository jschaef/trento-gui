import streamlit as st
from typing import Optional
import helpers.handle_support_file as hsf
def clb_text_input(col: Optional[st.delta_generator.DeltaGenerator], 
        warning:str) -> Optional[st.delta_generator.DeltaGenerator]:
    if not input:
        col.warning(warning)
    return 0

def clb_text_input_project_exists(col: Optional[st.delta_generator.DeltaGenerator], 
         user_name:str) -> Optional[st.delta_generator.DeltaGenerator]:
    project_name = st.session_state.get("project_name", None)
    if hsf.check_project_exists(project_name, user_name):
        col.warning("Project already exists, choose a different name")
        st.session_state["project_name_test"] = "_already_exists_"
    else:
        st.session_state.pop("project_name_test", None)