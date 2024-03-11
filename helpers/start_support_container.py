#!/usr/bin/python3

import os
import helpers.printer_help as p_help

def run_support_container(workspace: str, container_script_dir: str, 
        supportconfigs: list, placeholder: object)-> object:
    servers = []
    os.system(f"mkdir -p {workspace}")
    os.system(f"cp -av {container_script_dir}/* {workspace}")
    for supportconfig in supportconfigs:
        os.system(f"cp -av {supportconfig} {workspace}")
        supportconfig_bname = os.path.basename(supportconfig)
        server_name = supportconfig_bname.split('_')[1]
        servers.append(server_name)
    trento_str = "fb92284e-aa5e-47f6-a883-bf9469e7a0dc"
    servers = ' '.join(servers)
    supportconfigs = ' '.join(supportconfigs)
    script = f"""
#!/bin/bash
cd {workspace}
# create .container_def file
for server in "{servers}"; do
    machine_id=$(dbus-uuidgen)
    trento_agent_id=$(dbus-uuidgen -N $machine_id -n {trento_str} --sha1)

    cat <<HERE >>.container_def
$server:$machine_id:$trento_agent_id
HERE

    sleep 5
    for supportconfig in "{supportconfigs}"; do
        ./start_container  $supportconfig 
    done

done
"""

    ret = p_help.run_script(script, workspace, 'run_container.sh', placeholder)
    return ret

def test_cmd(workspace, place_holder):
    script = """
#!/bin/bash
    unset LANG
    ls -latrh upload
    find upload
    sleep 5
"""

    ret = p_help.run_script(script, workspace, 'run_test.sh', place_holder)
    return ret