import tarfile
import re
from os import path

def get_basic_information(archive_file:str):
    hardware = re.compile(b"^.*(Hardware|Manufacturer|Hypervisor|Identity):")
    hardware_dict = {}
    linux_line_prev = re.compile(b"^.*uname -a.*$")
    linux_line_found = 0
    collect_dict = {}
    target_file = "basic-environment.txt"
    target_path = f"{path.basename(archive_file).split('.')[0]}/{target_file}"

    with tarfile.open(archive_file,'r:xz') as archive_object:
        try:
            _ = archive_object.getmember(target_path)
        except KeyError as e:
            print(f"{target_path} could not be found, {e}")

        extracted_file = archive_object.extractfile(target_path)
        content = extracted_file.readlines()
        extracted_file.close()

    for line in content:
        match_0 = hardware.search(line)
        if match_0:
            hardware_dict[match_0.group(1).decode('utf-8')] = \
                line.decode('utf-8').strip().split(':')[1]  
            collect_dict['hardware'] = hardware_dict
        elif linux_line_prev.search(line):
            linux_line_found = 1
            continue
        elif linux_line_found:
            collect_dict['hostname'] = line.decode('utf-8').strip().split()[1]
            collect_dict['kernel'] = line.decode('utf-8').strip().split()[2]
            linux_line_found = 0

    return collect_dict
            
