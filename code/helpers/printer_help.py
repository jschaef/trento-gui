#!/usr/bin/python3
import subprocess
import streamlit as st
import config as Config
import helpers.log_handling as lgh
from os import chmod
from subprocess import CalledProcessError

Config = Config.Config()


def set_state_key(sess_key, value=None, change_key=None):
    if sess_key in st.session_state and st.session_state[sess_key][1] == change_key:
        return st.session_state[sess_key][0]
    else:
        st.session_state[sess_key] = [value, change_key]
        return st.session_state[sess_key][0]

def stdout_to_streamlit(trento_script_path, script, placeholder):
    ret_code = True
    with open(trento_script_path, 'w') as ts:
        ts.write(script)
    chmod(trento_script_path, 0o750)
    try:
        ret_code = lgh.execute(['/bin/bash', trento_script_path], placeholder)
    except CalledProcessError as e:
        placeholder.error(
            f'Execution of script failed with returncode {e.returncode}')
        return e.returncode
    subprocess.run(f'rm -rf {trento_script_path}', shell=True)
    return ret_code

def run_script(script,workspace, name, placeholder):
    trento_script_path = f'{workspace}/{name}'
    placeholder.code(script)
    return stdout_to_streamlit(trento_script_path, script, placeholder)

def stdout_to_streamlit_1(trento_script_path, script, placeholder):
    ret_code = True
    with open(trento_script_path, 'w') as ts:
        ts.write(script)
    chmod(trento_script_path, 0o750)
    try:
        ret_code, output, error_field = lgh.execute_1(['/bin/bash', trento_script_path])
    except CalledProcessError as e:
        placeholder.error(
            f'Execution of script failed with returncode {e.returncode}')
        return e.returncode, error_field
    subprocess.run(f'rm -rf {trento_script_path}', shell=True)
    return ret_code, output, error_field 

def run_script_1(script, workspace, name, placeholder):
    trento_script_path = f'{workspace}/{name}'
    placeholder.code(script)
    return stdout_to_streamlit_1(trento_script_path, script, placeholder)

def prg_stdout_val(cmd):
    ret = subprocess.run(cmd, capture_output=True, shell=True)
    return ret.stdout.decode()

def prg_retcode(cmd):
    ret = subprocess.run(cmd, shell=True, capture_output=False)
    return ret.returncode

def create_columns(number, write_field=None):
    """Create columns and write empty string into them
       if the column index in write_field is True
    Args:
        number (integer): number of columns
        write_field (list): 
    """
    cols = st.columns(number)
    if write_field:
        for entry in range(len(write_field)):
            if write_field[entry]:
                col = cols[entry]
                col.write('')
    return(cols)
