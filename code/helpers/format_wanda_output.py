import re
from streamlit.delta_generator import DeltaGenerator

def format_output(output: list, col: DeltaGenerator, 
    section: str, severity: str) -> None:
    """Format the output of the script.
    Args:
        output (list): list of strings
        col (DeltaGenerator): streamlit column
        section (str): section to filter
    Returns:
        None
    """

    sections = [
        "OS and package versions",
        "SBD",
        "Corosync",
        "Pacemaker",
        "saptune",
        "Azure Fence Agent",
        "Filesystems",
        "Sapservices",
        "SAP HANA System Replication Resource Agent ocf:suse:SAPHana",
        ]

    sub_sections = ["Remediation", "References"]
    severities = ["passing", "critical", "warning"]
    color_dict = {
        "passing": "green",
        "critical": "red",
        "warning": "orange",
    }

    indent = "&nbsp;"
    indent_val = 10
    id_field = ["hostname", "hostgroup", "agent id"]
    host_field = []

    if section != "all":
        output = filter_section(output, sections, section, col)
        sections.append(section)
    if severity != "all":
        output = filter_topic(output, severities, severity, section, sections)
        severities.append(severity)

    for line in output:
        line.strip()
        if any(re.match(f"^{section}$", line) for section in sections):
            col.markdown(f"#### {line}")
        elif any(re.match(f"^## {term}$", line) for term in sub_sections):
            line = re.sub(r"^## (.*)$", r"###### *\1*:", line)
            col.markdown(line)
        elif any(re.match(f"^\[{result}\].*", line) for result in severities):
            for result in severities:
                if re.match(f"^\[{result}\].*", line):
                    line = re.sub(rf"^\[({result})\](.*)$", rf"**\1** \2", line)
                    color = color_dict.get(result, "black")
                    line = f'<span style="color:{color}">{line}</span>'
                    col.markdown(line, unsafe_allow_html=True)
                    break
        elif any(re.match(f"^{id}:.*", line) for id in id_field):
            host_field.append(line)
            if len(host_field) == len(id_field):
                line = ", ".join(host_field)
                line = re.sub(r"^(.*)$", rf"{indent * indent_val}\1", line)
                col.write(line, unsafe_allow_html=True)
                host_field = []
        else:
            line = re.sub(r"^(.*)$", rf"{indent * indent_val}\1", line)
            col.write(line, unsafe_allow_html=True)

def filter_section(output: list, sections: list, section: str, col ) -> list:
    """Filter the output of the script.
    Args:
        output (list): list of strings
        sections (list): list of all available sections
        section (str): section to filter
    Returns:
        None
    """
    
    sections.remove(section) 
    return_field = []
    section_found = False

    for line in output:
        if any(re.match(f"^{section}$", line) for section in sections):
            section_found = False
            continue
        elif re.match(f"^{section}$", line):
            section_found = True
            return_field.append(line)
        elif section_found:
            return_field.append(line)
        else:
            continue
    return return_field

def filter_topic(output: list, severities:list, severity: str, 
        section: str, sections: list) -> list:
    """Filter the output of the script based on severities like critical.
    Args:
        output (list): list of strings
        severities (list): list of all available severities
        severity (str): severity to filter
        section (str): section to filter
        sections (list): list of all available sections
    Returns:
        list: list of strings
    """
    severities.remove(severity)
    return_field = []
    topic_found = False

    for line in output:
        if re.match(f"^{section}$", line):
            return_field.append(line)
        elif any(re.match(f"^\[{severity}\].*", line) for severity in severities):
            topic_found = False
            continue
        elif re.match(f"^\[{severity}\].*", line):
            topic_found = True
            return_field.append(line)
        elif topic_found:
            return_field.append(line)
        else:
            continue

    return return_field