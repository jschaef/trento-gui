import shutil
import subprocess
import re
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

    binaries = ["tcsc"]
    python_mods = ["polars", "docker", "defusedxml", "termcolor"]

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

def check_project_status(col: DeltaGenerator, project: str):
    """Check if the project is running by executing 'tcsc hosts status' command."""
    cmd = ["tcsc", "hosts", "status", project]
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')

    result = subprocess.run(cmd, capture_output=True, text=True)
    stdout = ansi_escape.sub('', result.stdout)
    stderr = ansi_escape.sub('', result.stderr)
    if result.returncode == 0:
        col.success(f"Project {project} is running")
        #col.code(stdout)
    else:
        col.error("Failed to check project status")
        col.code(stderr)
    return result.returncode

def run_checks(workspace: str, username: str, project: str, place_holder: DeltaGenerator)-> str:
    """Run the Trento checks
    
    arguments:
    username -- user's unique name
    project -- wanda groupname
    place_holder -- streamlit container
    Return: result (bool)
    """
    script = f"""
 #!/bin/bash
    unset LANG
    tcsc checks run {project}
    """
    ret = p_help.run_script(script, workspace, 'run_checks.sh', place_holder)