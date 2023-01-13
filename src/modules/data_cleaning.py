import pandas as pd
import logging
from modules import data_collection, constants
import _pickle as cPickle

def get_data(year: int):
    keepers = [
        pd.read_csv(f"../Data/FBREF_{year-1}"+"-"+f"{year-2000}"+"/" + f)
        for f in [f"keeper_{year-2000}.csv", f"keeper_adv_{year-2000}.csv"]
    ]
    players = [
        pd.read_csv(f"../Data/FBREF_{year-1}"+"-"+f"{year-2000}"+"/" + f)
        for f in [
            f"passing_{year-2000}.csv",
            f"possession_{year-2000}.csv",
            f"player_stats_{year-2000}.csv",
            f"misc_{year-2000}.csv",
            f"defense_{year-2000}.csv",
            f"shooting_{year-2000}.csv",
            #f"playing_time_{year-2000}.csv",
            f"passing_type_{year-2000}.csv",
            f"gsc_{year-2000}.csv",
            #f"keeper_{year-2000}.csv",
            #f"keeper_adv_{year-2000}.csv"
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
    fpl = data_collection.get_historic_fpl(year)[["first_name", "second_name", "now_cost", "element_type", "total_points"]]
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

    data_df = data_df.assign(
        Cost=data_df.Player.map(
            lambda x: fpl[fpl.Player == x].now_cost.values[0]
            if x in fpl.Player.to_list()
            else 0
        )
    )
    data_df = data_df.fillna(0)
    data_df = data_df.infer_objects()
    return data_df
