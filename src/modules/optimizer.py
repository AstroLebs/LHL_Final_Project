import _pickle as cPickle
import docplex
from docplex.mp.model import Model
import scipy
import numpy as np
from scipy.optimize import minimize
import pulp

# Thanks to Joseph O'Connor
"""expected_scores = df.predict_points
prices = df.now_cost / 10
position = df.element_type
team = df.team
names = df.web_name

decisions, captain_decisions, sub_decisions = select_team(
    expected_scores.values, prices.values, position.values, team.values
)"""


def select_team(
    expected_scores, prices, positions, clubs, total_budget=100, sub_factor=0.2
):
    num_players = len(expected_scores)
    
    model = pulp.LpProblem("Constrained_value_maximisation", pulp.LpMaximize)
    decisions = [
        pulp.LpVariable("x{}".format(i), lowBound=0, upBound=1, cat="Integer")
        for i in range(num_players)
    ]
    captain_decisions = [
        pulp.LpVariable("y{}".format(i), lowBound=0, upBound=1, cat="Integer")
        for i in range(num_players)
    ]
    sub_decisions = [
        pulp.LpVariable("z{}".format(i), lowBound=0, upBound=1, cat="Integer")
        for i in range(num_players)
    ]

    # objective function:
    print(len(expected_scores))
    model += (sum((captain_decisions[i] + decisions[i] + sub_decisions[i] * sub_factor)* expected_scores[i] for i in range(num_players)),"Objective",)
    
    #cost constraint
    model += sum((decisions[i] + sub_decisions[i]) * prices[i] for i in range(num_players)) <= total_budget  
        # total cost
    
    
    # position constraints
    # 1 starting goalkeeper
    model += sum(decisions[i] for i in range(num_players) if positions[i] == 1) == 1
    
    # 2 total goalkeepers
    model += sum(
            decisions[i] + sub_decisions[i]
            for i in range(num_players)
            if positions[i] == 1
        ) == 2
    

    # 3-5 starting defenders
    model += sum(decisions[i] for i in range(num_players) if positions[i] == 2) >= 3
    model += sum(decisions[i] for i in range(num_players) if positions[i] == 2) <= 5
    # 5 total defenders
    model += sum(
            decisions[i] + sub_decisions[i]
            for i in range(num_players)
            if positions[i] == 2
        ) == 5
    

    # 3-5 starting midfielders
    model += sum(decisions[i] for i in range(num_players) if positions[i] == 3) >= 3
    model += sum(decisions[i] for i in range(num_players) if positions[i] == 3) <= 5
    # 5 total midfielders
    model += sum(
            decisions[i] + sub_decisions[i]
            for i in range(num_players)
            if positions[i] == 3
        ) == 5
    
    # 1-3 starting attackers
    model += sum(decisions[i] for i in range(num_players) if positions[i] == 4) >= 1
    model += sum(decisions[i] for i in range(num_players) if positions[i] == 4) <= 3
    # 3 total attackers
    model += sum(
            decisions[i] + sub_decisions[i]
            for i in range(num_players)
            if positions[i] == 4
        ) == 3
    

    # club constraint
    for club_id in np.unique(clubs):
        model += sum(
                decisions[i] + sub_decisions[i]
                for i in range(num_players)
                if clubs[i] == club_id
            ) <= 3
          # max 3 players

    model += sum(decisions) == 11  # total team size
    model += sum(captain_decisions) == 1  # 1 captain

    for i in range(num_players):
        model += decisions[i] - captain_decisions[i] >= 0  
        # captain must also be on team
        model += (decisions[i] + sub_decisions[i]) <= 1  # subs must not be on team

    model.solve()

    return decisions, captain_decisions, sub_decisions
