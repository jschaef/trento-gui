import streamlit as st
from os import system
import helpers.visual_funcs as visf
import helpers.handle_users as user_mgmt
import helpers.tcsc_checks as tcsc_checks
import config as cfg

def admin_menu(cols: st.columns):
    col1, *_ = cols
    header_ph = col1.empty()
    header_container = header_ph.container()
    header_container.header('Admin Service')
    menu_items = ["Check Environment", "Container Service", "Trento Service", "User Management",]
    choice = header_container.radio('Take your Choice',menu_items)
    header_container.write('___')
    if choice == 'Container Service':
        container_service()
    elif choice == 'User Management':
        user_service()
    elif choice == 'Trento Service':
        trento_service()
    elif choice == 'Check Environment':
        check_environment()

def check_environment():
    cols = visf.create_columns(4, [0,1,1,1])
    col1 = cols[0]
    env_check = tcsc_checks.check_environment(col1)
    if not env_check:
        col1.warning("Please correct the environment issues first")
    
def container_service():
    cols = visf.create_columns(4, [0,1,1,1])
    col1 = cols[0]
    col1.subheader('Container Management')
    menu_items = ['Show Containers', 'Delete Containers',]
    choice = col1.selectbox('Take your Choice',menu_items)

def trento_service():
    cols = visf.create_columns(4, [0,1,1,1])
    col1 = cols[0]
    col1.subheader('Trento Management')
    menu_items = ['Update Trento', 'Uninstall Trento', ]
    container_items = ['all', 'wanda_container', 'cmd_container', 'hosts_container']
    choice = col1.selectbox('Take your Choice',menu_items)
    visf.make_vspace(1, col1)

    if choice == 'Update Trento':
        cols = st.columns([0.2,0.1,0.6])
        col1 = cols[0]
        col2 = cols[1]
        col3 = cols[2]
        col1.markdown('##### Update Trento')
        col1.write('Do you want to update the git repo?')
        update_git_repo = col1.radio('Update Git Repo', ['Yes', 'No'], help="""
        Without updating the git repo containers will just be removed and new installed""",
        horizontal=True, index=1)
        if update_git_repo == 'No':
            cont_choice = col1.selectbox('Choose Container(s) to update', container_items)
            visf.make_vspace(5, col1)
            if col1.button(f'Update {cont_choice}'):
                pass

def update_trento():
    pass

def uninstall_trento():
    pass

def pull_git_repo():
    pass

def show_containers():
    pass

def delete_containers():
    pass

def user_service():
    cols = visf.create_columns(4, [0,1,1,1])
    col1 = cols[0]
    col1.subheader('User Management')
    menu_items = ['Show Users', 'User Password Change', 'Roles Management', 
        'Delete User', 'Login History']
    choice = col1.selectbox('Take your Choice',menu_items)
    if choice == 'Show Users':
         col1.dataframe(user_mgmt.view_all_users('show'), )    
    else:
        user_ph = col1.empty()
        user = user_ph.selectbox('Choose User', user_mgmt.view_all_users(kind=None))
    if choice == 'User Password Change':
        col1.subheader(f'Change Password of {user}')
        password = col1.text_input("Type the new password:", type='password')
        re_password = col1.text_input("Retype your new password:", type='password')
        if st.button('Submit'):
            if password == re_password and password:
                user_mgmt.change_password(user, password)
                col1.info(f'Password of {user} has been Changed')
            elif not password:
                col1.warning("empty password is not allowed")
            else:
                col1.warning("The passwords do not match") 
    elif choice == 'Roles Management':
        visf.make_vspace(1, col1)
        col1.markdown(f'##### Change Role of {user}')
        if user != 'admin':
            r_content = col1.selectbox('Choose role', user_mgmt.get_roles())
            if st.button('Submit'):
                user_mgmt.change_role(user, r_content)
                col1.info(f'Role {r_content} for {user} has been set')
        else:
            col1.warning('Role for admin cannot be changed')
    elif choice == 'Delete User':
        if user != 'admin':
            upload_dir = f'{cfg.Config.UPLOAD_DIR}/{user}'
            col1.subheader(f'Delete User {user}')
            if st.button('Submit'):
                user_mgmt.delete_user(user)
                if user in upload_dir:
                    system(f'rm -rf {upload_dir}')
                col1.info(f'User {user} has been deleted')
        else:
            col1.warning('User admin cannot be deleted')
    elif choice == 'Login History':
        user_ph.empty()
        col1.subheader('Show Login times for users')
        df_pl = user_mgmt.get_user_status_df()
        df = df_pl.to_pandas().set_index('login_time')
        col1.dataframe(df)
        del_help = 'Delete all login times older than the chosen date'
        if col1.checkbox('Delete Login Times', help=del_help):
            delete_date = col1.date_input('Choose Date', value=None, min_value=None, max_value=None, key=None)
            if col1.button('Delete'):
                result = user_mgmt.remove_old_logins(df_pl, delete_date)
                if not result.is_empty():
                    user_mgmt.write_df_to_file(result)
                    col1.info(f'''Records older than {delete_date} 
                        have been deleted''')
                    col1.write('Remaining Records:')
                    col1.write(result.to_pandas().set_index('login_time'))
                else:
                    df_pl = user_mgmt.create_user_status_df()
                    user_mgmt.write_df_to_file(df_pl)