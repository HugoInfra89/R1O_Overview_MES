import pandas as pd

data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 28],
    'City': ['New York', 'San Francisco', 'Los Angeles']
}

df = pd.DataFrame(data)


def make_excel_file(dataframe):
    from openpyxl import Workbook
    from openpyxl.utils.dataframe import dataframe_to_rows
    wb = Workbook()
    ws = wb.active

    ws.title = "My New Worksheet"

    for row in dataframe_to_rows(dataframe, index=False, header=False):
        print(row)
        ws.append(row)

    ws.column_dimensions["A"].width = 20
    wb.save("py_test.xlsx")

make_excel_file(df)