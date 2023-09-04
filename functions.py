import os as os
from pathlib import Path
import pandas as pd

def choose_project_area():
    prj_area_options = ["OWR","R1O"]
    user_input = ""
    while user_input not in prj_area_options:
        user_input = "R1O"


        import time
        print(f"User input = {user_input}")
        time.sleep(2)

        #user_input = input(f"For which project area do you want to see the model data? [{prj_area_options[0]}/{prj_area_options[-1]}]: ").upper()
    project_area_dict = {   "OWR":"(000)_OWR",
                            "R1O":"(050)_R1O"}
    return (user_input,project_area_dict[user_input])


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


def check_model_files(dataframe, model_type="DMO", file_type=".nwc"):
    """
    :param dataframe: A dataframe containing at least the object_code, BMO_files, bools.
    :param model_type: The model type DMO or DMM.
    :param file_type: The suffix of the filetypes that has been checked in this function.
    :return: returns a dictionary with a series of checked filenames and bools
    """
    select_dataframe = dataframe[["object_code", "BMO_files", "check_name_BMO", f"{model_type}_{file_type}"]]

    model_list = select_dataframe[f"{model_type}_{file_type}"].dropna().tolist()
    ds_BMO_files = select_dataframe["BMO_files"].dropna()

    bool_model_list = []
    true_model_list = []

    for i, item in ds_BMO_files.items():
        BMO_object_code = item.split("-")[1]
        BMO_serie_number = item.split("-")[-1].split(".")[0]
        bool_code_check = False
        true_model_name = ""
        for model_name in model_list:
            object_code_model = model_name.split("-")[1]
            serie_code_model = model_name.split("-")[-1].split(".")[0]
            if BMO_object_code == object_code_model and BMO_serie_number == serie_code_model:
                true_model_name = model_name
                bool_code_check = True

        true_model_list.append(true_model_name)
        bool_model_list.append(bool_code_check)

    ds_true_model = pd.Series(data=true_model_list, dtype=str, name=f"real_{model_type}_{file_type}", copy=True)
    ds_bool_model = pd.Series(data=bool_model_list, dtype=bool, name=f"bool_{model_type}_{file_type}", copy=True)
    dataseries = {f"filenames_{model_type}_{file_type}": ds_true_model, f"bools_{model_type}_{file_type}": ds_bool_model}

    print(f"filenames_{model_type}_{file_type}")
    print(f"bools_{model_type}_{file_type}")
    return dataseries



