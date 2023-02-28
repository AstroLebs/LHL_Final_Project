from modules.data_cleaning import get_data
from modules.models import model
import modules.optimizer as optimizer
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
    
    test_df = test_df[test_df.Cost != 0]
    xFP = test_df.drop(['Player','Cost','FPL_points'], axis = 1).reset_index(drop=True).T.reset_index(drop=True).T
    expected_scores = mod.predict(xFP)
    prices = (test_df.Cost / 10).to_list()
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

    with open('../output/teamlist.txt', 'w') as f:
        f.write('Starting 11: \n')
        predict_total = 0
        real_total = 0
        for i in range(len(decisions)):
            if decisions[i].value() != 0:
                f.write(f'{names[i]} {pos_map[position[i]]}: {round(float(expected_scores[i]), 2)} points predicted at ${prices[i]} ')
                if captain_decisions[i].value() == 1:
                    f.write('TEAM CAPTAIN')
                    real_total += test_df[test_df.Player == names[i]].FPL_points.values[0]
                    predict_total += expected_scores[i]
                f.write('\n')    
                real_total += test_df[test_df.Player == names[i]].FPL_points.values[0]
                predict_total += expected_scores[i]
        
        f.write('\n \nSubs:\n')
        for j in range(len(sub_decisions)):
            if sub_decisions[j].value() != 0:
                f.write(f'{names[j]} {pos_map[position[j]]}: {round(float(expected_scores[i]), 2)} points at ${prices[j]} \n')

        f.write(f'\n \nPredicted Point Total: {round(predict_total, 2)} \n')
        f.write(f'Real Point Total: {real_total} \n')





if __name__ == "__main__":
    main()
