import pandas as pd
import logging
import numpy as np
import pickle
from modules import constants
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

slim_team_df = team_df[
    [
        "short_name",
        "code",
        "strength_overall_home",
        "strength_overall_away",
        "strength_attack_home",
        "strength_attack_away",
        "strength_defence_home",
        "strength_defence_away",
    ]
]
slim_pos_df = pos_df.drop(
    [
        "plural_name",
        "singular_name",
        "plural_name_short",
        "ui_shirt_specific",
        "sub_positions_locked",
        "element_count",
    ],
    axis=1,
)
slim_player_df = player_df[
    [
        "chance_of_playing_next_round",
        "chance_of_playing_this_round",
        "code",
        "element_type",
        "ep_next",
        "ep_this",
        "event_points",
        "form",
        "id",
        "now_cost",
        "points_per_game",
        "selected_by_percent",
        "squad_number",
        "status",
        "team",
        "team_code",
        "total_points",
        "value_form",
        "value_season",
        "web_name",
        "minutes",
        "goals_scored",
        "assists",
        "clean_sheets",
        "goals_conceded",
        "own_goals",
        "penalties_saved",
        "penalties_missed",
        "yellow_cards",
        "red_cards",
        "saves",
        "bonus",
        "bps",
        "influence",
        "creativity",
        "threat",
        "ict_index",
        "starts",
        "expected_goals",
        "expected_assists",
        "expected_goal_involvements",
        "expected_goals_conceded",
        "influence_rank",
        "influence_rank_type",
        "creativity_rank",
        "creativity_rank_type",
        "threat_rank",
        "threat_rank_type",
        "ict_index_rank",
        "ict_index_rank_type",
        "corners_and_indirect_freekicks_order",
        "direct_freekicks_order",
        "penalties_order",
        "expected_goals_per_90",
        "saves_per_90",
        "expected_assists_per_90",
        "expected_goal_involvements_per_90",
        "expected_goals_conceded_per_90",
        "goals_conceded_per_90",
        "now_cost_rank",
        "now_cost_rank_type",
        "form_rank",
        "form_rank_type",
        "points_per_game_rank",
        "points_per_game_rank_type",
        "selected_rank",
        "selected_rank_type",
        "starts_per_90",
        "clean_sheets_per_90",
    ]
]

slim_player_df = convert_to_float(slim_player_df)
slim_player_df = slim_player_df.dropna(how="all", axis=1)
slim_player_df = slim_player_df.fillna(0)
slim_player_df.status = slim_player_df.status.map(
    {
        "i": "injury",
        "u": "unavailable",
        "d": "decision",
        "a": "available",
        "s": "suspect",
    }
)


with open(r"../Data/players.pickle", "wb") as output_file:
    cPickle.dump(slim_player_df, output_file)

with open(r"../Data/position.pickle", "wb") as output_file:
    cPickle.dump(slim_pos_df, output_file)

with open(r"../Data/team.pickle", "wb") as output_file:
    cPickle.dump(slim_team_df, output_file)
