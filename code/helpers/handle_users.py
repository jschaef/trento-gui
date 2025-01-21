import datetime
import os
import user
import streamlit as st
import polars as pl
import config as cfg

USER_LOGIN_FILE = "user_login.parquet"

def view_all_users(kind: str):
    user_file = cfg.Config.USERS_FILE
    user_df = user.load_user_file(user_file).drop('password')
    if kind == 'show':
        return user_df
    else:
        return user_df['user_name'].to_list()

def change_password(user_name: str, password: str):
    user_file = cfg.Config.USERS_FILE
    enc_pass = user.encrypt_password(password)
    df = user.load_user_file(user_file)
    df =df.with_columns(
        password=pl.when(pl.col('user_name')==user_name)
                .then(pl.lit(enc_pass))
                .otherwise(pl.col("password")))
    df.write_parquet(user_file)
    st.session_state.user_df = df
    return df

def change_role(user_name: str, user_role: str):
    user_file = cfg.Config.USERS_FILE
    df = user.load_user_file(user_file)
    df =df.with_columns(
        role=pl.when(pl.col('user_name')==user_name)
                .then(pl.lit(user_role))
                .otherwise(pl.col("role")))

    df.write_parquet(user_file)
    st.session_state.user_df = df
    return df

def get_roles():
    user_file = cfg.Config.USERS_FILE
    df = user.load_user_file(user_file)
    roles = df['role'].unique().to_list()
    required_roles = ['admin', 'user']
    for role in required_roles:
        if role not in roles:
            roles.append(role)
    return roles

def delete_user(user_name: str):
    user_file = cfg.Config.USERS_FILE
    df = user.load_user_file(user_file)
    user.delete_user(df, user_name, user_file)


def load_df_from_file(
    filename: str = USER_LOGIN_FILE,
) -> pl.DataFrame:
    df = pl.DataFrame()
    if not os.path.exists(filename):
        df = create_user_status_df()
        write_df_to_file(df, filename)
    return pl.read_parquet(filename)

def write_df_to_file(df: pl.DataFrame, filename: str = USER_LOGIN_FILE) -> None:
    df.write_parquet(filename)


def delete_records(df: pl.DataFrame, date: datetime.datetime) -> pl.DataFrame:
    """Deletes records from the dataframe where login_time is greater than the provided date.
    Args:
        df: The dataframe to delete the records from
        date: The date to compare with
    Returns:
        The dataframe with the deleted records
    """
    df = df.filter(df["login_time"] <= date)
    write_df_to_file(df)

def create_user_status_df() -> pl.DataFrame:
    """Creates prefilled dataframe including metadata about
    user login times.
    Args:
        None
    Returns:
        A dataframe with the following columns:
            - user_name: The user's unique ID
            - login_time: When did the user login last time
            - user_status: Does the user exist in the database
    """
    return pl.DataFrame(
        {
            "user_name": ["admin"],
            "login_time": [datetime.datetime.now()],
            "success": [True],
        }
    )

def add_record(
    user_name: str,
    login_time: datetime.datetime,
    success: bool,
    filename: str = USER_LOGIN_FILE,
) -> pl.DataFrame:
    """Adds a record to the dataframe.
    Args:
        df: The dataframe to add the record to
        user_name: The user's unique ID
        login_time: When did the user login last time
        success: could the user login
    """
    df = get_user_status_df()
    df1 = pl.DataFrame(
        {
            "user_name": [user_name],
            "login_time": [login_time],
            "success": [success],
        }
    )
    df = df.vstack(df1)
    df.write_parquet(filename)

def get_user_status_df() -> pl.DataFrame:
    """Gets the dataframe with the user status.
    Args:
        None
    Returns:
        The dataframe with the user status
    """
    df = load_df_from_file()
    return df

def remove_old_logins(df: pl.DataFrame, date: datetime.date) -> pl.DataFrame:
    df = df.filter(pl.col("login_time") > date)
    return df