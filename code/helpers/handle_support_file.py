import json
import re
import polars as pl
from datetime import datetime
from os import path, getcwd, listdir, system
import config as cfg

def create_support_df(user_name: str) -> pl.DataFrame:
    """
    Creates initial support parquet dataframe for the user
    Args:
        user_name: The user's unique name

    Returns:
        pl.DataFrame: containing all support config information
    """
    
    # Define the schema with empty columns
    return pl.DataFrame(
        {
            "user_name": pl.Series([], dtype=pl.Utf8),
            "support_configs": pl.Series([], dtype=pl.List(pl.Utf8)),
            "project": pl.Series([], dtype=pl.Utf8),
            "basic_environment": pl.Series([], dtype=pl.Utf8),
            "check_results": pl.Series([], dtype=pl.List(pl.Utf8)),
            "container_state": pl.Series([], dtype=pl.Boolean),
            "creation_time": pl.Series([], dtype=pl.Datetime),
        }
    )
    
def load_support_file(user_name: str) -> pl.DataFrame:
    """load parquet file containing all support config 
    of the respective user information

    Args:
        user_name (str): The user's unique name

    Returns:
        pl.DataFrame: dataframe for the user
    """
    base_dir = getcwd()
    upload_dir = f"{base_dir}/{cfg.Config.UPLOAD_DIR}/{user_name}/support_files"
    if not path.isdir(upload_dir):
        system(f'mkdir -p {upload_dir}')
    support_file = f"{upload_dir}/{user_name}_scf.parquet"
    if not path.exists(support_file):
        df =  create_support_df(user_name)
        df.write_parquet(support_file)
    return pl.read_parquet(support_file), support_file

def get_support_config_files(upload_dir: str) -> list:
    """Get all unprocessed support config files for the user

    Args:
        user_name (str): The user's unique name

    Returns:
        list: list of support config files
    """
    pattern = re.compile(r"^scc_.*\.txz$")
    support_files = [ x for x in listdir(upload_dir) if path.isfile(f'{upload_dir}/{x}')
        and pattern.match(x)]
    return support_files

def initial_update_support_file(user_name: str, pl_support_file: str,
        support_configs: list, project: str, basic_env: str) -> None:
    """Update the polars support config file for the user

    Args:
        user_name (str): The user's unique name
        pl_support_file (str): The parquet support file to update
        support_configs (list): The list of support config files
        project (str): The project name
    """

    df = pl.read_parquet(pl_support_file)
    # Create a new DataFrame with the new record
    new_record = pl.DataFrame(
        {
            "user_name": [user_name],
            "support_configs": [support_configs],
            "project": [project],
            "basic_environment": [json.dumps(basic_env)],  # Add default values for other columns
            "check_results": [[""]],
            "container_state": [True],
            "creation_time": [datetime.now()],
        }
    )
    # Concatenate the new record with the existing DataFrame
    updated_df = pl.concat([df, new_record])

    # Write the updated DataFrame back to the parquet file
    updated_df.write_parquet(pl_support_file)

def get_projects(user_name: str) -> list:
    """Get all projects for the user

    Args:
        user_name (str): The user's unique name

    Returns:
        list: list of projects
    """
    df, _ = load_support_file(user_name)
    return df.select("project").unique().to_series().to_list()

def add_wanda_check_results(user_name: str, check_results: list, project: str) -> pl.DataFrame:
    """Add the wanda check results to the support file

    Args:
        user_name (str): The user's unique name
        check_results (list): The list of check results
        project (str): The project name

    Returns:
        pl.DataFrame: The updated support file
    """
    # Get the user name
    df, support_file = load_support_file(user_name)
    # Update the check results for the specified project

    df = df.with_columns(
        pl.when(pl.col("project") == project)
        .then(pl.lit(check_results))
        .otherwise(pl.col("check_results"))
        .alias("check_results")
    )

    # Write the updated DataFrame back to the parquet file
    df.write_parquet(support_file)
    return df

def is_check_results_empty(user_name: str, project: str) -> bool:
    """Check if the check_results column for a given project contains an empty list.

    Args:
        user_name (str): The user's unique name
        project (str): The project name

    Returns:
        bool: True if the check_results column contains an empty list, False otherwise
    """
    df, _ = load_support_file(user_name)
    result = df.filter((pl.col("project") == project) & (pl.col("check_results").list.len() > 0))
    return result.is_empty()


def get_check_results(user_name: str, project: str) -> list:
    """Get the content of the check_results column for a given project.

    Args:
        user_name (str): The user's unique name
        project (str): The project name

    Returns:
        list: The content of the check_results column for the given project
    """
    df, _ = load_support_file(user_name)
    result = df.filter(pl.col("project") == project).select("check_results")
    if not result.is_empty():
        return result["check_results"].first()
    return []

def delete_project_record(user_name: str, project: str) -> pl.DataFrame:
    """Delete the record for a given project from the support file.

    Args:
        user_name (str): The user's unique name
        project (str): The project name

    Returns:
        pl.DataFrame: The updated support file
    """
    df, support_file = load_support_file(user_name)
    # Filter out the record with the specified project
    updated_df = df.filter(pl.col("project") != project)
    # Write the updated DataFrame back to the parquet file
    updated_df.write_parquet(support_file)
    return updated_df

def check_project_exists(project_name:str, user_name: str) -> bool:
    """Check if a project exists in the support file

    Args:
        project_name (str): The project name
        user_name (str): The user's unique name

    Returns:
        bool: True if the project exists, False otherwise
    """

    user_project_list = get_projects(user_name)
    return project_name in user_project_list