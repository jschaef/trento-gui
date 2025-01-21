import streamlit as st
from menu import menu_with_redirect
import helpers.admin_service as admin_service

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

# Verify the user's role
if not st.session_state.get("user_role", None) == "admin":
    st.warning("You are not authorized to view this page.")
    menu_with_redirect()

else:
    cols = st.columns(4)
    admin_service.admin_menu(cols) # Render the admin service