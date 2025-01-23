import streamlit as st

def authenticated_menu():
    st.sidebar.page_link("pages/5_📂manage supportconfigs.py", label="Upload supportconfigs", 
        icon="🔼")
    st.sidebar.page_link("pages/8_🔍trento_checks.py", label="Check supportconfig with Trento", 
        icon="🏁")
    if st.session_state.get("user_role", None) in ["admin"]:
        st.sidebar.page_link("pages/4_👩‍✈️admin.py", label="Admin tasks",
            disabled=st.session_state.user_role !="admin", icon="👩‍✈️")

def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    menu_with_redirect()


def menu():
    # Determine if a user is logged in or not, then show the correct
    # navigation menu
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        unauthenticated_menu()
        return
    authenticated_menu()


def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to
    # render the navigation menu
    if "login_task"  in st.session_state:
        if st.session_state.login_task == "signup":
            st.switch_page("pages/2_📝signup.py")
        elif st.session_state.login_task == "login":
            st.switch_page("pages/1_👩‍💻login.py")
    else:
        st.switch_page("pages/1_👩‍💻login.py")