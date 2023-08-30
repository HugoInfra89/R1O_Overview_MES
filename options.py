import pandas as pd

#This is a code which arranges the pandas view settings
def set_options_for_pandas():
    pd.set_option("display.max_columns", 6)
    pd.set_option('display.max_colwidth', 200)
    pd.set_option('display.width', 1000)

