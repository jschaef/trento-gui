import polars as pl
from os import path, getcwd, listdir
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
            "check_results": pl.Series([], dtype=pl.Utf8),
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
    support_file = f"{upload_dir}/{user_name}_scf.parquet"
    if not path.exists(support_file):
        df =  create_support_df(user_name)
        df.write_parquet(support_file)
    return pl.read_parquet(support_file)

def get_support_config_files(upload_dir: str) -> list:
    """Get all unprocessed support config files for the user

    Args:
        user_name (str): The user's unique name

    Returns:
        list: list of support config files
    """
    support_files = [ x for x in listdir(upload_dir) if path.isfile(f'{upload_dir}/{x}')]
    return support_files