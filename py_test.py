import pandas as pd
from functions import make_dictionary_lantis_relatics_for_mapping

make_dictionary_lantis_relatics_for_mapping()

print("End of Script")


def make_meta_data():
    import datetime as dt
    current_datetime = dt.datetime.now()
    formatted_time = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    print(formatted_time)



make_meta_data()
