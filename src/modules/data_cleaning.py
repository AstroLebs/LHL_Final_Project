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


def fbref_player():
    keepers = [
        pd.read_csv("../Data/FBREF_2020-21/" + f)
        for f in ["keeper_21.csv", "keeper_adv_21.csv"]
    ]
    players = [
        pd.read_csv("../Data/FBREF_2020-21/" + f)
        for f in [
            "passing_21.csv",
            "possession_21.csv",
            "player_stats_21.csv",
            "misc_21.csv",
            "defense_21.csv",
            "shooting_21.csv",
            # "playing_time_21.csv",
            "passing_type_21.csv",
            "gsc_21.csv",
        ]
    ]
    data_df = players[0]
    for df in players[1:]:
        data_df = pd.concat([data_df, df], axis=1)

    data_df = data_df.T.drop_duplicates().T
    data_df.drop(
        ["Rk", "Nation", "Pos", "Born", "Matches", "-9999"], axis=1, inplace=True
    )

    # Replace w/ data_collection
    fpl = pd.read_csv("../Data/FPL_22.csv")[
        ["first_name", "second_name", "element_type", "total_points"]
    ]
    fpl = fpl.assign(Player=fpl.first_name + " " + fpl.second_name).drop(
        ["first_name", "second_name"], axis=1
    )

    data_df = data_df.assign(
        FPL_points=data_df.Player.map(
            lambda x: fpl[fpl.Player == x].total_points.values[0]
            if x in fpl.Player.to_list()
            else 0
        )
    )
    data_df = data_df.infer_objects()

    return data_df
