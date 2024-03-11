import streamlit as st
import polars as pl
import helpers.hashing
import config as cfg
from datetime import datetime
from os import path

def create_user_file(filename: str):
    admin_pass = cfg.Config.ADMIN_PASS
    admin_pass_enc = encrypt_password(admin_pass)
    df =  pl.DataFrame(
        {
            "user_name": ["admin"],
            "creation_time": [datetime.now()],
            "password": [admin_pass_enc],
            "role": ["admin"],
        }
    )
    df.write_parquet(filename)

def find_user_file(filename: str):
    cur_dir = path.dirname(path.realpath(__file__))
    fpath = f"{cur_dir}/{filename}"
    if path.isfile(fpath):
        return fpath
    else:
        create_user_file(filename)
        return fpath

def load_user_file(filename: str) -> pl.DataFrame:
    if "user_df" in st.session_state:
        return st.session_state.user_df 
    df_file = find_user_file(filename)
    df = pl.read_parquet(df_file)
    st.session_state.user_df = df
    return df

def add_user(df: pl.DataFrame, username: str, password: str, 
        filename: str) -> pl.DataFrame:
    """Adds a record to the dataframe.
    Args:
        df: The dataframe to add the record to
        user_name: The user's unique ID
        password: The user's password
        the df_file for persistence
    """
    df1 = pl.DataFrame(
        {
            "user_name": [username],
            "creation_time": [datetime.now()],
            "password": [password],
            "role": "user",
        }
    )
    df = df.vstack(df1)
    df.write_parquet(filename)
    st.session_state.user_df = df
    return df

def delete_user(df: pl.DataFrame, username: str, filename: str):
    df = df.filter(pl.col("user_name") != username)
    df.write_parquet(filename)
    st.session_state.user_df = df
    return df

def encrypt_password(password: str) -> str:
    enc_pass = helpers.hashing.hash_password(password)
    return enc_pass
    
def check_user(df: pl.DataFrame, username: str, password: str) -> bool:
    stored_pwd = df.filter(pl.col("user_name") == username).select(pl.col("password"))
    if stored_pwd.shape[0] != 0:
        stored_pwd = stored_pwd["password"][0]
    else:
        return [False,  False]
    if helpers.hashing.verify_password(stored_pwd, password):
        return [True, True]
    else:
        return [False, True]

def user_exists(df: pl.DataFrame, username: str) -> bool:
    return df.filter(pl.col("user_name") == username).shape[0] > 0

def get_user_role(user_file: str, username: str,) -> str:
    df = load_user_file(user_file)
    role = df.filter(pl.col("user_name") == username).select(pl.col("role"))
    role = role["role"][0]
    return role


def signup(user_file) -> tuple[bool, str]:
    df = load_user_file(user_file)
    st.subheader("Create an Account")
    col1, _ = st.columns([0.2, 0.8])
    new_user = col1.text_input("Username")
    new_password = col1.text_input("Password", type='password')
    if user_exists(df, new_user):
        col1.warning(f"User {new_user} already exists, choose another username")
        return False, new_user
    encrypted_password = encrypt_password(new_password)
    if st.button("Signup"):
        add_user(df, new_user, encrypted_password, user_file)
        col1.info(f"User {new_user} created successfully")
        return True, new_user
    else:
        st.stop()

def login(filename: str, col: st.columns ) -> tuple[str, str]:
    col = col or st.columns(1)
    df = load_user_file(filename)
    st.subheader("Login")
    col1, _ = st.columns([0.2, 0.8])
    username = col1.text_input("Username")
    password = col1.text_input("Password", type='password')
    if st.button("Login"):
        if username and password:
            if all(check_user(df, username, password)):
                st.session_state.logged_in = True
                return "logged_in", username
            elif user_exists(df, username):
                if not all(check_user(df, username, password)):
                    return "user_password_wrong", username
            else:
                return "user_not_exists", username
        else:
            return "invalid_input", username
    else:
        st.stop()