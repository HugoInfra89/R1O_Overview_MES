def save_data_to_sharepoint(dataframe):
        folderpath_to_temp_folder = r"C:\Users\hvanegeraat\AppData\Local\Temp"
        file_name = "Overview MES.xlsx"

        path_temp_excel_file = rf"{folderpath_to_temp_folder}\{file_name}"
        dataframe.to_excel(path_temp_excel_file, sheet_name="Overview MES", index=False)

        from openpyxl import load_workbook

        wb = load_workbook(path_temp_excel_file)
        ws = wb.active

        ws.column_dimensions["A"].width = 15
        ws.column_dimensions["B"].width = 20
        ws.column_dimensions["C"].width = 50

        modelname_columns = ["D","F","H","J","L","N"]
        for model_column_name in modelname_columns:
                ws.column_dimensions[model_column_name].width = 40

        bool_columns = ["E", "G", "I", "K", "M", "O"]
        for bool_col_name in bool_columns:
                ws.column_dimensions[bool_col_name].width = 20

        folderpath_sharepoint = r"C:\Users\hvanegeraat\THV ROCO\R1O (050) - 04 BIM\Overview objects ES R1O\All MES overview R1O"
        path_sharepoint = rf"{folderpath_sharepoint}\{file_name}"
        print(path_sharepoint)
        wb.save(path_sharepoint)

        import os
        os.system(f'start excel "{path_sharepoint}"')

