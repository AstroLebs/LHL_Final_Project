import modules.optimizer as optimizer


def initial_team(mod, df):
    """
    Return team decisions based on initial model and player data
    :Args:
    :mod: trained model
    :df: dataframe for model prediciton

    :Return:
    :team_decisions: 11 Starting Players
    :captain_decisions: Top scoring starter
    :sub_decisions: 4 Bench players (1 Keeper, 3 Others)
    :inputs: tuple of args passed to optimizer
    """
    df = df[df.Cost != 0]
    xFP = df.drop(['Player', 'Cost', 'FPL_points'], axis=1)
    xFP = xFP.reset_index(drop=True).T.reset_index(drop=True).T
    expected_scores = mod.predict(xFP)
    prices = (df.Cost / 10).to_list()
    pos = df.Position.map({'GK': 1, 'DEF': 2, 'MID': 3, 'FWD': 4}).to_list()
    team = df.Squad.to_list()
    names = df.Player.to_list()
    inputs = (expected_scores, prices, pos, team, names)
    team_decisions, captain_decisions, sub_decisions =\
        optimizer.select_team(expected_scores, prices, pos, team)
    return team_decisions, captain_decisions, sub_decisions, inputs
