import os as os
from pathlib import Path
import pandas as pd

def make_dictionary_for_mapping():
    """

    """
    new_dict = {}
    stems = ["R1_Oost", "R1_Oost_Context"]
    csv_filepaths = ["data/Onderliggend_R1_Oost.csv", "data/Onderliggend_R1_Oost_Context.csv"]
    for stem in stems:
        path = f"data/Onderliggend_{stem}.csv"
        dataframe = pd.read_csv(path)
        value_arr = dataframe.values

        for item in value_arr:
            splitted_item = item[0].split(" - ")
            new_dict[splitted_item[0].replace("Obj-", "")] = (stem, splitted_item[1])
    return new_dict


def get_export_files(path):
    """
    This function reads the files in a specific folder. After the files will be sorted by their suffixes. A dataframe
    will be returned including the following columns:
        - Column with the DMO_.nwc filenames [DMO_.nwc]
        - Column with the DMO_.ifc filenames [DMO_.ifc]
        - Column with the DMO_.dwg filenames [DMO_.dwg]
        - Column with the DMM_.dwg filesnames [DMM_.dwg]
        - Column with other filenames [DMO_other]
    """
    path_DMO = path
    contents = os.listdir(path_DMO)

    file_list_DMO_nwc = []
    file_list_DMM_nwc = []
    file_list_ifc = []
    file_list_DMO_dwg = []
    file_list_DMM_dwg = []
    file_list_else = []
    for file_name in contents:
        file = Path(file_name)
        str_file_name = str(file)
        try:
            model_type = str_file_name.split("-")[3]
        except:
            print("Splitting not possible")
            breakpoint()
        if file.suffix == ".nwc" and model_type == "DMO":
            file_list_DMO_nwc.append(file_name)
        elif file.suffix == ".nwc" and model_type == "DMM":
            file_list_DMM_nwc.append(file_name)
        elif file.suffix == ".ifc":
            file_list_ifc.append(file_name)
        elif file.suffix == ".dwg" and model_type == "DMO":
            file_list_DMO_dwg.append(file_name)
        elif file.suffix == ".dwg" and model_type == "DMM":
            file_list_DMM_dwg.append(file_name)
        else:
            file_list_else.append(file_name)

    ds_DMO_nwc = pd.Series(file_list_DMO_nwc, name="DMO_.nwc")
    ds_DMM_nwc = pd.Series(file_list_DMM_nwc, name="DMM_.nwc")
    ds_ifc = pd.Series(file_list_ifc, name="DMO_.ifc")
    ds_DMO_dwg = pd.Series(file_list_DMO_dwg, name="DMO_.dwg")
    ds_DMM_dwg = pd.Series(file_list_DMM_dwg, name="DMM_.dwg")
    ds_else = pd.Series(file_list_else, name="DMO_other")

    df_sorted_models = pd.concat([ds_DMO_nwc, ds_DMM_nwc, ds_ifc, ds_DMO_dwg, ds_DMM_dwg, ds_else], axis="columns")

    return df_sorted_models


def check_model_files(dataframe, filetype="DMO_.nwc"):
    """
    :param dataframe: A dataframe containing at least the object_code, BMO_files, bools,
    :param filetype: The suffix of the filetypes that has been checked in this function.
    :return: returns a dictionary with a series of checked filenames and bools
    """
    select_dataframe = dataframe[["object_code", "BMO_files", "check_name_BMO", f"DMO_{filetype}"]]

    DMO_list = select_dataframe[f"DMO_{filetype}"].dropna().tolist()
    ds_object_codes = select_dataframe["object_code"].dropna()

    bool_DMO_list = []
    true_DMO_list = []

    for i, item in ds_object_codes.items():
        object_code_BMO = item
        bool_code_check = False
        true_DMO_name = "No DMO available"
        for DMO_name in DMO_list:
            object_code_DMO = DMO_name.split("-")[1]
            if object_code_BMO == object_code_DMO:
                true_DMO_name = DMO_name
                bool_code_check = True

        true_DMO_list.append(true_DMO_name)
        bool_DMO_list.append(bool_code_check)

    ds_true_DMO = pd.Series(data=true_DMO_list, dtype=str, name=f"real_DMO{filetype}", copy=True)
    ds_bool_DMO = pd.Series(data=bool_DMO_list, dtype=bool, name=f"bool_DMO{filetype}", copy=True)
    dataseries = {f"filenames_{filetype}" : ds_true_DMO, f"DMO_bools_{filetype}" : ds_bool_DMO}

    return dataseries



