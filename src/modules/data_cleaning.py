import pandas as pd
import logging
from modules import data_collection, constants
import _pickle as cPickle


def convert_to_float(data):
    for col in data:
        if data[col].dtype == "int":
            continue
        data[col] = data[col].astype("string")
        try:
            data[col] = data[col].astype("float")
        except ValueError as e:
            logging.exception(f"{col}: e")

    return data


data = data_collection.FPL_Data_Collection()
player_df = pd.DataFrame(data.get_player_data())
team_df = pd.DataFrame(data.get_team_data())
pos_df = pd.DataFrame(data.get_positional_data())
