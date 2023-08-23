import os as os
import pandas as pd
import xlwings as xw
from functions import get_export_files, check_DMO_files, make_dictionary_for_mapping

from options import set_options_for_pandas
set_options_for_pandas()

path_BMO = r"C:\Users\hvanegeraat\DC\ACCDocs\Lantis\Lantis 3B\Project Files\002_WIP\W200_Bestaande toestand\W200.TT41 BT Constructies\(050)_R1O"
path_DMO = r"C:\Users\hvanegeraat\DC\ACCDocs\Lantis\Lantis 3B\Project Files\002_WIP\W200_Bestaande toestand\W200.TT41 BT Constructies\(050)_R1O"

# List all files and folders within the folder
contents = os.listdir(path_BMO)

# Iterate over the contents in the BMO-files on BIM360 and add only the file names to the list.
list_BMO_files = []
for item in contents:
    item_path = os.path.join(path_BMO, item)
    if os.path.isfile(item_path):
        list_BMO_files.append(item)

# Convert the list of the BMO models to a data series
ds_BMO_models = pd.Series(list_BMO_files)

# This part of code is checking the convention of the build-up of the BMO files
check_name_list = []
for i, name in pd.Series(ds_BMO_models).items():
    splitted_name = name.split("-")
    if splitted_name[0] == "OWRB" and splitted_name[2] in ["ROC", "LAN"] and splitted_name[3] in ["BMO", "TMO"] and splitted_name[4] == "W66":
        ds_name = splitted_name[5].split(".")
        if isinstance(ds_name[0], str) and ds_name[1] == "rvt":
            check_name_list.append(True)
        else:
            check_name_list.append(False)
    else:
        check_name_list.append(False)

# This part of code makes a dataframe of the list of bools which checked the convention of the  names
ds_check_names = pd.Series(check_name_list)
df_BMO_overview = pd.concat([ds_BMO_models, ds_check_names], axis="columns", keys=["BMO_files", "check_name_BMO"])


# This part of the code isolates the object number of the name BMO-filenames
object_list = []
for value in df_BMO_overview["BMO_files"]:
    sp_value = value.split("-")[1]
    object_list.append(sp_value)


# This part of code makes a series of the list of object numbers
ds_object_code = pd.Series(object_list, name="object_code")

#  In this step the object names will be mapped to the existing object names
dict_objects_name_num = make_dictionary_for_mapping()
ds_object_name = ds_object_code.map(dict_objects_name_num).fillna("Unknown").rename("object_name")

df_object_code_name = pd.concat([ds_object_code, ds_object_name], axis="columns")

df_BMO_overview = pd.concat([df_object_code_name, df_BMO_overview], axis="columns")

df_DMO_overview = get_export_files(path=path_DMO)

df_model_overview = pd.concat([df_BMO_overview, df_DMO_overview], axis="columns")
df_model_overview.drop(columns="DMO_other", inplace=True)


filenames_and_bools_nwc = check_DMO_files(dataframe=df_model_overview, filetype=".nwc")

name_nwc = filenames_and_bools_nwc["filenames_.nwc"]
bool_nwc = filenames_and_bools_nwc["DMO_bools_.nwc"]

filenames_and_bools_ifc = check_DMO_files(dataframe=df_model_overview, filetype=".ifc")
name_ifc = filenames_and_bools_ifc["filenames_.ifc"]
bool_ifc = filenames_and_bools_ifc["DMO_bools_.ifc"]


filenames_and_bools_dwg = check_DMO_files(dataframe=df_model_overview, filetype=".dwg")
name_dwg = filenames_and_bools_dwg["filenames_.dwg"]
bool_dwg = filenames_and_bools_dwg["DMO_bools_.dwg"]

df = pd.concat([df_BMO_overview, name_nwc, bool_nwc, name_ifc, bool_ifc, name_dwg, bool_dwg], axis=1)
xw.view(df)

 