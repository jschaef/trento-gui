#!/usr/bin/python3

import helpers.printer_help as p_help
import helpers.tcsc_checks as tcsc_checks
from streamlit.delta_generator import DeltaGenerator

def start_containers(workspace: str, place_holder: DeltaGenerator,
        support_files: list, wanda_dict: dict)-> bool:
    """Start the supportconfig containers
    
    arguments:
    workspace -- file to place the script
    place_holder -- streamlit container
    support_files -- list of supportconfig files
    wanda_dict -- dictionary with wanda information like:
        * project (wanda groupname)
        * provider
        * cluster_type (ensa1, ensa2, mixed_versions)
        * filesystem_type
        * architecture_type
        * hana_scenario
    Return: result (bool)
    """

    project = wanda_dict.pop("project")
    wanda_env = " ".join([f"{key}={value}" for key, value in wanda_dict.items()])
    if wanda_env:
        wanda_env = f"-e {wanda_env}"
    else:
        wanda_env = ""
    
    support_files = " ".join(support_files)
    script = f"""
 #!/bin/bash
    unset LANG
    tcsc hosts create {project} {wanda_env} {support_files}
    """

    ret = p_help.run_script(script, workspace, 'start_containers.sh', place_holder)