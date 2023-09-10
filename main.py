import os as os
import pandas as pd
import xlwings as xw
from functions import (get_export_files, check_model_files, make_dictionary_for_mapping, choose_project_area,
                       make_dictionary_lantis_relatics_for_mapping)
from func_dat_pres import data_presentation
from func_save import save_data_to_local, open_from_local_and_modify, save_bar_chart_on_sharepoint

from options import set_options_for_pandas
set_options_for_pandas()

project_code_tuple = choose_project_area()
project_area = project_code_tuple[0]
project_area_code = project_code_tuple[1]

#Determining the folderpath based user input
folder_path = rf"C:\Users\hvanegeraat\DC\ACCDocs\Lantis\Lantis 3B\Project Files\002_WIP\W200_Bestaande toestand\W200.TT41 BT Constructies\{project_area_code}"


#List all files and folders within the folder
contents = os.listdir(folder_path)

#Iterate over the contents in the BMO-files on BIM360 and add only the file names to the list.
list_BMO_files = []
for item in contents:
    item_path = os.path.join(folder_path, item)
    if os.path.isfile(item_path) and item.split(".")[1] == "rvt":
        list_BMO_files.append(item)

#Convert the list of the BMO models to a data series
ds_BMO_models = pd.Series(list_BMO_files)

#This part of code is checking the convention of the build-up of the BMO files
check_name_list = []
for i, name in pd.Series(ds_BMO_models).items():
    splitted_name = name.split("-")
    if splitted_name[0] == "OWRB" and splitted_name[2] in ["ROC", "LAN"] and splitted_name[3] in ["BMO", "TMO"] and splitted_name[4] in ["W66", "W27"]:
        ds_name = splitted_name[5].split(".")
        if isinstance(ds_name[0], str) and ds_name[1] == "rvt":
            check_name_list.append(True)
        else:
            check_name_list.append(False)
    else:
        check_name_list.append(False)

#This part of code makes a dataframe of the list of bools which checked the convention of the  names
ds_check_names = pd.Series(check_name_list)
df_BMO_overview = pd.concat([ds_BMO_models, ds_check_names], axis="columns", keys=["BMO_files", "check_name_BMO"])


#This part of the code isolates the object number of the name BMO-filenames
object_list = []
for value in df_BMO_overview["BMO_files"]:
    sp_value = value.split("-")[1]
    object_list.append(sp_value)


#This part of code makes a series of the list of object numbers
ds_object_code = pd.Series(object_list, name="object_code")

#In this step the object names will be mapped to the existing object names
dict_objects_name_num = make_dictionary_for_mapping()

#Seperate the stem and object name in one dictionary
stem_dict = {key: value[0] for key, value in dict_objects_name_num.items()}
object_name_dict = {key: value[1] for key, value in dict_objects_name_num.items()}

#Make a dataseries for the descriptions and root of the OBS
ds_object_stem = ds_object_code.map(stem_dict).fillna("Unknown").rename("object_stem")
ds_object_name = ds_object_code.map(object_name_dict).fillna("Unknown").rename("object_name")


#Mapping the Data of the Lantis Relatics
dict_lantis = make_dictionary_lantis_relatics_for_mapping()
ds_BMO_names_map = df_BMO_overview["BMO_files"].str.split(".").str[0]
ds_lantis_relatics = ds_BMO_names_map.map(dict_lantis).rename("lantis_ID")

df_object_code_name = pd.concat([ds_object_code, ds_lantis_relatics, ds_object_stem, ds_object_name], axis="columns")

df_BMO_overview = pd.concat([df_object_code_name, df_BMO_overview], axis="columns")
df_model_overview = get_export_files(path=folder_path)

df_all_model_overview = pd.concat([df_BMO_overview, df_model_overview], axis="columns")
df_all_model_overview.drop(columns="DMO_other", inplace=True)


#DMO_NWC
filenames_and_bools_DMO_nwc = check_model_files(dataframe=df_all_model_overview, model_type="DMO", file_type=".nwc")
name_DMO_nwc = filenames_and_bools_DMO_nwc["filenames_DMO_.nwc"]
bool_DMO_nwc = filenames_and_bools_DMO_nwc["bools_DMO_.nwc"]

#DMM_NWC
filenames_and_bools_DMM_nwc = check_model_files(dataframe=df_all_model_overview, model_type="DMM", file_type=".nwc")
name_DMM_nwc = filenames_and_bools_DMM_nwc["filenames_DMM_.nwc"]
bool_DMM_nwc = filenames_and_bools_DMM_nwc["bools_DMM_.nwc"]

#DMO_IFC
filenames_and_bools_DMO_ifc = check_model_files(dataframe=df_all_model_overview, model_type="DMO", file_type=".ifc")
name_DMO_ifc = filenames_and_bools_DMO_ifc["filenames_DMO_.ifc"]
bool_DMO_ifc = filenames_and_bools_DMO_ifc["bools_DMO_.ifc"]

#DMO_DWG
filenames_and_bools_DMO_dwg = check_model_files(dataframe=df_all_model_overview, model_type="DMO", file_type=".dwg")
name_DMO_dwg = filenames_and_bools_DMO_dwg["filenames_DMO_.dwg"]
bool_DMO_dwg = filenames_and_bools_DMO_dwg["bools_DMO_.dwg"]

#DMM_DWG
filenames_and_bools_DMM_dwg = check_model_files(dataframe=df_all_model_overview, model_type="DMM", file_type=".dwg")
name_DMM_dwg = filenames_and_bools_DMM_dwg["filenames_DMM_.dwg"]
bool_DMM_dwg = filenames_and_bools_DMM_dwg["bools_DMM_.dwg"]


df = pd.concat([df_BMO_overview,
                name_DMO_nwc,
                bool_DMO_nwc,
                name_DMM_nwc,
                bool_DMM_nwc,
                name_DMO_ifc,
                bool_DMO_ifc,
                name_DMO_dwg,
                bool_DMO_dwg,
                name_DMM_dwg,
                bool_DMM_dwg],
               axis="columns")

bar_chart = data_presentation(dataframe=df)


# Do you want to save the data on sharepoint
user_input = ""
user_input = input("Do you want to update the data to Sharepoint? [Yes/No]: ").upper()
if user_input == "YES":
    save_data_to_local(dataframe=df)
    open_from_local_and_modify(project_data=project_code_tuple)
    save_bar_chart_on_sharepoint(plt=bar_chart)
else:
    print("Data is not saved ... ")

