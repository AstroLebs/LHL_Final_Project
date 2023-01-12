from modules.data_cleaning import get_data
from modules.models import model
import pickle

def main():
    year = 2022
    try:
        with open(f"../output/pickles/{year-1}.pickle", 'rb') as input_train:
            train_df = pickle.load(input_train)
    except (FileNotFoundError, OSError) as e:
        train_df = get_data(year-1)
        with open(f"../output/pickles/{year-1}.pickle",'wb') as output_train:
            pickle.dump(train_df, output_train)

    try:
        with open(f"../output/pickles/{year}.pickle", 'rb') as input_test:
            test_df = pickle.load(input_test)
    except (FileNotFoundError, OSError) as e:
        test_df = get_data(year)
        with open(f"../output/pickles/{year}.pickle",'wb') as output_test:
            pickle.dump(test_df, output_test)
    # Load Datasets

    try:
        with open(f"../output/pickles/{year}_model.pickle", 'rb') as input_model:
            mod = pickle.load(input_model)
    except (FileNotFoundError, OSError) as e:
        mod, y_pred, mse, rmse, r2 = model(train_df.drop(["Player","Cost"], axis=1))
        with open(f"../output/pickles/{year}_model.pickle",'wb') as output_model:
            pickle.dump(mod, output_model)
    
    expected_scores = mod.predict(test_df.drop(["Player","Cost","FPL_points"], axis = 1))
    prices = (test_df.now_cost / 10).to_list()
    position = test_df.Position.map({'GK':1, 'DEF':2, 'MID':3, 'FWD':4}).to_list()
    team = test_df.Squad.to_list()
    names = test_df.Player.to_list()

    decisions, captain_decisions, sub_decisions = optimizer.select_team(
    expected_scores, prices, position, team
    )

    


    # Load / Run Year Start Model
    # Optimize Year Start Result
    # Return
    # Check for New Data
    # Run Week-to-Week Model to look for Transfers
    # Optimize Transfer Suggestions
    # Return

    pos_map = {1:'GK', 2:'DEF', 3: 'MID', 4:'FWD'}
    team_names = []
    with open('../output/teamlist.txt', 'w') as f:
        f.write('Starting 11')
        for i in range(len(decisions)):
            if decisions[i].value() != 0:
                team_names.append(names[i])
                f.write(f'{names[i]} {pos_map[position[i]]}: {expected_scores[i]} points at ${prices[i]}')
        f.write('Subs')
        for i in range(len(sub_decisions)):
            if sub_decisions[i].value() != 0:
                team_names.append(names[i])
                f.write(f'{names[i]} {pos_map[position[i]]}: {expected_scores[i]} points at ${prices[i]}')




if __name__ == "__main__":
    main()
