import re
from streamlit.delta_generator import DeltaGenerator
def format_output(output: list, col: DeltaGenerator):
    """Format the output of the script.
    Args:
        output (list): list of strings
        col (DeltaGenerator): streamlit column
    Returns:
        None
    """

    sections = [
        "OS and package versions",
        "SBD",
        "Corosync",
        "Pacemaker",
        "saptune",
        ]

    sub_sections = ["Remediation", "References"]
    results = ["passing", "critical", "warning"]
    critical = ["critical"]
    color_dict = {
        "passing": "green",
        "critical": "red",
        "warning": "orange",
    }

    indent = "&nbsp;"
    indent_val = 10
    id_field = ["hostname", "hostgroup", "agent id"]
    host_field = []

    for line in output:
        line.strip()
        if any(re.match(f"^{section}$", line) for section in sections):
            col.markdown(f"#### {line}")
        elif any(re.match(f"^## {term}$", line) for term in sub_sections):
            line = re.sub(r"^## (.*)$", r"###### *\1*:", line)
            col.markdown(line)
        # elif any(re.match(f"^[{result}.*", line) for result in critical):
        #     line = re.sub(r"^([critical])(.*)$", rf"f'<span style='color:red'>\1</span>' \2", line)
        #     col.markdown(line, unsafe_allow_html=True)
        # elif any(re.match(f"^\[{result}\].*", line) for result in results):
        #     line = re.sub(r"^(.*)$", rf"###### \1", line)
        #     col.markdown(line)
        elif any(re.match(f"^\[{result}\].*", line) for result in results):
            for result in results:
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