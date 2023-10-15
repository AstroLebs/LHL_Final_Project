from modules.data_cleaning import get_data
from modules.models import model
from modules.initial_team import initial_team
from modules.print_teamlist import print_teamlist
import os

# import modules.optimizer as optimizer
import pickle


def main():
    os.chdir("src/")
    year = 2023
    try:
        with open(f"../output/pickles/{year-1}.pickle", "rb") as input_train:
            train_df = pickle.load(input_train)
    except (FileNotFoundError, OSError):
        train_df = get_data(year - 1)
        with open(f"../output/pickles/{year-1}.pickle", "wb") as output_train:
            pickle.dump(train_df, output_train)

    try:
        with open(f"../output/pickles/{year}.pickle", "rb") as input_test:
            test_df = pickle.load(input_test)
    except (FileNotFoundError, OSError):
        test_df = get_data(year)
        with open(f"../output/pickles/{year}.pickle", "wb") as output_test:
            pickle.dump(test_df, output_test)
    # Load Datasets
    columns = test_df.columns.intersection(train_df.columns).tolist()

    try:
        with open(f"../output/pickles/{year}_model.pickle", "rb") as in_model:
            mod = pickle.load(in_model)
    except (FileNotFoundError, OSError):

        mod, y_pred, mse, rmse, r2 = model(
            train_df[columns].drop(["Player", "Cost"], axis=1)
        )
        with open(f"../output/pickles/{year}_model.pickle", "wb") as output_model:
            pickle.dump(mod, output_model)

    (
        decisions,
        captain_decisions,
        sub_decisions,
        inputs,
        final_player_list,
    ) = initial_team(mod, test_df[columns])

    final_player_list.to_csv(
        f"../output/{year}_predictions.csv", index=False, header=False
    )

    # Load / Run Year Start Model
    # Optimize Year Start Result
    # Return
    # Check for New Data
    # Run Week-to-Week Model to look for Transfers
    # Optimize Transfer Suggestions
    # Return

    print_teamlist(test_df, decisions, captain_decisions, sub_decisions, inputs, year)


if __name__ == "__main__":
    main()
