import xlwings as xw
import matplotlib.pyplot as plt

def data_presentation(dataframe):
    df_sel = dataframe[["object_code", "BMO_files", "real_DMO.nwc", "real_DMO.ifc", "real_DMO.dwg"]]
    df_sel_bool = dataframe[["object_code", "check_name_BMO", "bool_DMO.nwc", "bool_DMO.ifc", "bool_DMO.dwg"]]
    print(dataframe.columns)
    print(df_sel_bool)
    print("Hi")

    count_all_object_numbers = df_sel_bool["object_code"].count()
    count_unique_object_numbers = df_sel_bool["object_code"].nunique()
    count_BMOs = df_sel_bool["check_name_BMO"].sum()
    count_DMO_nwc = df_sel_bool["bool_DMO.nwc"].sum()
    count_DMO_ifc = df_sel_bool["bool_DMO.ifc"].sum()
    count_DMO_dwg = df_sel_bool["bool_DMO.dwg"].sum()

    print(f"count_all_object_numbers: {count_all_object_numbers}")
    print(f"count_unique_object_numbers: {count_unique_object_numbers}")
    print(f"count_BMOs: {count_BMOs}")
    print(f"count_DMO_nwc: {count_DMO_nwc}")
    print(f"count_DMO_ifc: {count_DMO_ifc}")
    print(f"count_DMO-dwg: {count_DMO_dwg}")

    categories = ['count_BMOs', 'count_DMO_nwc', 'count_DMO_ifc', 'count_DMO_dwg']
    values = [count_BMOs, count_DMO_nwc, count_DMO_ifc, count_DMO_dwg]

    # Create a bar chart
    plt.bar(categories, values)

    # Add labels and title
    plt.xlabel('Categories')
    plt.ylabel('Values')
    plt.title('Bar Chart Example')

    xw.view(dataframe)


    # Display the chart
    plt.show()