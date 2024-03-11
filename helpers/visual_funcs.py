import streamlit as st

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

def make_grid(col: st.columns, col1_numbers: int, col2_numbers: int,
        col1_position: int, res_cols: tuple) -> tuple:
    """Returns two columns with the given numbers of rows.
       col: streamlit columns object 
       col1_numbers: number of level 1 cols in the columns object
       col2_numbers: number of columns to create in the col1_position column of the col object 
       col1_position: position of the column where the second level of columns 
            should be created
       res_cols: tuple with two numbers, to determine which columns to return
            from the col object
    """         
    cols_level_one = col.columns(col1_numbers)
    remaining_cols = cols_level_one[col1_position:]
    preciding_cols = cols_level_one[:col1_position]
    cols_level_two = cols_level_one[col1_position].columns(col2_numbers)
    col1, col2 = res_cols
    t_col1 = cols_level_two[col1]
    t_col2 = cols_level_two[col2]
    return t_col1, t_col2, preciding_cols, remaining_cols

def make_vspace(size: int, col: object) -> None:
    col.write(f"{size * '#'}")

def make_big_vspace(size:int, col: object) -> None:
    for x in range(size):
        make_vspace(1, col)

