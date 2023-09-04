import xlwings as xw
import matplotlib.pyplot as plt

def data_presentation(dataframe, prj_area="(050)_R1O"):

    df_sel = dataframe[["object_code",
                        "BMO_files",
                        "real_DMO_.nwc",
                        "real_DMM_.nwc",
                        "real_DMO_.ifc",
                        "real_DMO_.dwg",
                        "real_DMM_.dwg"]]

    df_sel_bool = dataframe[["object_code",
                             "check_name_BMO",
                             "bool_DMO_.nwc",
                             "bool_DMM_.nwc",
                             "bool_DMO_.ifc",
                             "bool_DMO_.dwg",
                             "bool_DMM_.dwg"]]

    count_all_object_numbers = df_sel_bool["object_code"].count()
    count_unique_object_numbers = df_sel_bool["object_code"].nunique()
    count_BMOs = df_sel_bool["check_name_BMO"].sum()
    count_DMO_nwc = df_sel_bool["bool_DMO_.nwc"].sum()
    count_DMM_nwc = df_sel_bool["bool_DMM_.nwc"].sum()
    count_DMO_ifc = df_sel_bool["bool_DMO_.ifc"].sum()
    count_DMO_dwg = df_sel_bool["bool_DMO_.dwg"].sum()
    count_DMM_dwg = df_sel_bool["bool_DMM_.dwg"].sum()

    print(f"count_all_object_numbers: {count_all_object_numbers}")
    print(f"count_unique_object_numbers: {count_unique_object_numbers}")
    print(f"count_BMOs: {count_BMOs}")
    print(f"count_DMO_nwc: {count_DMO_nwc}")
    print(f"count_DMM_nwc: {count_DMM_nwc}")
    print(f"count_DMO_ifc: {count_DMO_ifc}")
    print(f"count_DMO_dwg: {count_DMO_dwg}")
    print(f"count_DMM_dwg: {count_DMM_dwg}")

    categories = ['BMO.rvt', 'DMO.nwc', 'DMM.nwc', 'DMO.ifc', 'DMO.dwg', 'DMM.dwg']
    values = [count_BMOs, count_DMO_nwc, count_DMM_nwc, count_DMO_ifc, count_DMO_dwg, count_DMM_dwg]
    labels = categories
    custom_colors = ["navy", "darkgreen", "green", "red", "darkorange", "orange"]

    # Create a bar chart
    for i in range(len(categories)):
        plt.bar(categories[i],
                values[i],
                label=labels[i],
                color=custom_colors[i],
                width=0.6,
                edgecolor = 'black',
                linewidth=1,
                alpha=0.9)

    # Add labels and title
    plt.xlabel('Modellen')
    plt.ylabel('Hoeveelheid')
    title_text = f"Overzicht modellen voor {prj_area.split('_')[-1]}"
    plt.title(title_text)
    plt.grid(axis="y")
    plt.legend()

    xw.view(dataframe)

    # Display the chart
    plt.show()