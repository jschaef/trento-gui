import streamlit as st

def authenticated_menu():
    st.sidebar.page_link("pages/📂supportconfigs-upload.py", label="Upload supportconfigs", 
        icon="🔼")
    st.sidebar.page_link("pages/🔨trento_checks.py", label="Check supportconfig with Trento", 
        icon="🏁")
    if st.session_state.get("role", None) in ["admin", "super-admin"]:
        st.sidebar.page_link("pages/admin.py", label="Manage users")
        st.sidebar.page_link(
            "pages/super-admin.py",
            label="Manage admin access",
            disabled=st.session_state.role != "super-admin",
        )
    #st.switch_page("pages/supportconfigs-upload.py")


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
        if st.session_state.login_task == "login":
            st.switch_page("pages/👩‍💻login.py")
        elif st.session_state.login_task == "signup":
            st.switch_page("pages/📝signup.py")
        elif st.session_state.get("role", None):
            st.switch_page("app.py")

    #menu()