import requests
import pandas as pd
from modules.constants import FPL_URL, FPL_HIST, FBREF_SEARCH_URL, FBREF_PLAYER_LABELS


def get_current_fpl(as_json=False):
    """
    Calls the FPL's API to get this years data
    """
    with requests.Session() as s:
        r = s.get(url=FPL_URL)
        json = r.json()
    if as_json:
        return json

    player_df = pd.DataFrame(json["elements"])
    team_df = pd.DataFrame(json["teams"])
    pos_df = pd.DataFrame(json["element_types"])

    return player_df, team_df, pos_df

def get_historic_fpl(year: int):
    """
    Reads historic FPL from vaastav records hosted on github
    """    
    url = FPL_HIST + str(year - 1) + "-" + str(year - 2000) + "/cleaned_players.csv"
    return_df = pd.read_csv(url)

    return return_df


def player_search(player_name: str):
    """
    Searches FBREF for a playerand returns similar players
    """
    tables = pd.read_html(FBREF_SEARCH_URL + player_name.replace(" ", "+"))
    table_num = len(tables)
    scout_num = int((table_num - 9) / 2)
    table_names = []
    for i in range(scout_num):
        table_names.append(f"scout_{i}")
        table_names.append(f"similar_{i}")
        table_names.sort()

    table_names += FBREF_PLAYER_LABELS
    return dict(zip(table_names, tables))


def get_fbref_team():
    """
    Returns team and vs team data
    """
    raw_data = pd.read_html(FBREF_URLS)

    raw_data[1].columns = raw_data[1].columns.map(lambda x: f"{x[0]}_{x[1]}")
    squad = pd.merge(
        raw_data[0],
        raw_data[1],
        left_index=True,
        right_index=True,
    )
    opponents = None

    for i, table in enumerate(raw_data[2:]):
        try:
            table.columns = table.columns.map(lambda x: f"{x[0]}_{x[1]}")
        except Exception as e:
            pass

        if i % 2 == 0:
            squad = pd.merge(
                squad, table, left_on="Squad", right_on="Unnamed: 0_level_0_Squad"
            )
        else:
            if opponents is None:
                opponents = table
                continue
            else:
                opponents = pd.merge(
                    opponents,
                    table,
                    left_on="Unnamed: 0_level_0_Squad",
                    right_on="Unnamed: 0_level_0_Squad",
                )

    squad = squad.T.drop_duplicates().T
    opponents = opponents.T.drop_duplicates().T
    
    return squad, opponents
