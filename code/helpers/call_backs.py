import streamlit as st
from typing import Optional
def clb_text_input(col: Optional[st.delta_generator.DeltaGenerator], 
        warning:str) -> Optional[st.delta_generator.DeltaGenerator]:
    if not input:
        col.warning(warning)
    return 0