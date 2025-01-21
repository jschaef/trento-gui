import polars as pl
import helpers.visual_funcs as visf
from os import path, listdir, system
from magic import from_buffer
import helpers.handle_support_file as hsf

def file_mngmt(upload_dir: str):
    col1, _, _ = visf.create_columns(3,[0,1,])
    if not path.isdir(upload_dir):
        system(f'mkdir -p {upload_dir}')
    manage_files = ['Show Supportconfig Files','Add Supportconfig Files', 'Delete Supportconfig Files']
    #support_files = [ x for x in listdir(upload_dir) if path.isfile(f'{upload_dir}/{x}')]
    support_files = hsf.get_support_config_files(upload_dir)
    file_size = [path.getsize(f'{upload_dir}/{x}') for x in support_files]
    managef_options = col1.selectbox(
        'Show/Add/Delete', manage_files)

    if managef_options == 'Add Supportconfig Files':
        support_files = [col1.file_uploader(
        "Please upload your supportconfig files, ", key='file_uploader',
        accept_multiple_files=True)]
        if col1.button('Submit'):
            if support_files:
                link_check = 0
                for multi_files in support_files:
                    for u_file in multi_files:
                        if u_file is not None:
                            bytes_data = u_file.read()
                            res = from_buffer(bytes_data)
                            if "XZ compressed data" not in res:
                                col1.warning(
                                    f'File is not a valid xz file. Instead {res}')
                                continue
                            else:
                                col1.write(
                                    f"supportconfig file seems to be valid. Saving {u_file.name}")
                                with open(f'{upload_dir}/{u_file.name}', 'wb') as targetf:
                                    targetf.write(bytes_data)
                                    link_check = 1
                if link_check == 1:
                    visf.make_vspace(1, col1)
                    col1.page_link("pages/🔨trento_checks.py", label="Go to Trento Checks",
                        icon="🔨")

    elif managef_options == 'Delete Supportconfig Files':
        if support_files:
            dfiles_ph = col1.empty()
            dfiles = dfiles_ph.multiselect(
                'Choose your Files to delete', support_files, default=None)
            if col1.button('Delete selected Files'):
                for file in dfiles:
                    df_file = f'{upload_dir}/{file}'
                    system(f'rm -f {df_file}')
                support_files = listdir(upload_dir)
                dfiles = dfiles_ph.multiselect(
                    'Choose your Files to delete', support_files, default=None)
        else:
            col1.write("You currently have no supportconfig files to delete")

    elif managef_options == 'Show Supportconfig Files':
        col1.empty()
        fsize = [f'{round(x/1024/1024,2)} MB' for x in file_size]
        col1.dataframe(pl.DataFrame({'Files':support_files, 'Size':fsize}))

 