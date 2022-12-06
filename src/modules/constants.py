# API URLS
FPL_URL = "https://fantasy.premierleague.com/api/bootstrap-static/"
FPL_HIST = (
    "https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/"
)

FBREF_URLS = "https://fbref.com/en/comps/9/2021-2022/2021-2022-Premier-League-Stats"
FBREF_SEARCH_URL = "https://fbref.com/search/search.fcgi?search="
FBREF_PLAYER_LABELS = [
    "standard_stats",
    "shooting",
    "passing",
    "pass_types",
    "goal_shot",
    "defensive",
    "possession",
    "playing_time",
    "misc",
]
FBREF_TEAM_LABELS = [
    "regular_season_overall",
    "regular_season_homeaway",
    "standard_squad",
    "standard_opponent",
    "goalkeeping_squad",
    "goalkeeping_opponent",
    "goalkeeping_adv_squad",
    "goalkeeping_adv_opponent",
    "shooting_squad",
    "shooting_opponent",
    "passing_squad",
    "passing_opponent",
    "pass_type_squad",
    "pass_type_opponent",
    "goal_shot_creation_squad",
    "goal_shot_creation_opponent",
    "defensive_action_squad",
    "defensive_action_opponent",
    "possession_squad",
    "possession_opponent",
    "playtime_squad",
    "playtime_opponent",
    "misc_squad",
    "misc_opponent",
]

FPL_TEAM = [
    [
        "code",
        "name",
        "strength_overall_home",
        "strength_overall_away",
        "strength_attack_home",
        "strength_attack_away",
        "strength_defence_home",
        "strength_defence_away",
    ]
]

FPL_POS = [["id", "plural_name"]]

FPL_PLAYER = [
    [
        "code",
        "element_type",
        "first_name",
        "id",
        "now_cost",
        "status",
        "team",
        "total_points",
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
        "influence",
        "creativity",
        "threat",
        "starts",
        "expected_goals",
        "expected_assists",
        "expected_goal_involvements",
        "expected_goals_conceded",
    ]
]
