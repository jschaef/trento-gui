import shutil
import importlib
import helpers.printer_help as p_help
from streamlit.delta_generator import DeltaGenerator

def check_environment(col: DeltaGenerator) -> bool:
    """Check if the environment is set up correctly.
    Args:
        None
    Returns:
        bool: True if the environment is set up correctly
    """

    binaries = ["who", "man", "ls", "find", "sleep",]
    #python_mods = ["polars", "docker", "defusedxml", "termcolor"]
    python_mods = ["polars"]

    col.write("***Checking environment*** ...")
    for binary in binaries:
        col.markdown(f"Checking for binary {binary} ...")
        if shutil.which(binary) is None:
            col.warning(f"{binary} not found in PATH")
            return False
    col.info("Environment is set up correctly")

    col.write("***Checking python modules*** ...")
    for mod in python_mods:
        col.markdown(f"Checking for Python module {mod} ...")
        if importlib.util.find_spec(mod) is None:
            col.warning(f"Python module {mod} not found")
            return False
    col.info("All required Python modules are installed")
    return True

def check_wanda(col: DeltaGenerator, workspace: str) -> bool:
    script = """
#!/bin/bash
    unset LANG
    tcsc wanda status
"""
    ret = p_help.run_script(script, workspace, 'wanda-status.sh', col)