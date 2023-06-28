import pandas
import pickle
from modules import get_historic_fpl

def clean_scout(filename: str):
    file_path = '../Data/' + filename
    with open(file_path, 'rb') as f:
        scout_data = pickle.load(f)

    fpl_data = get_historic_fpl(int(filename[0:4]))
    print(f'FPL length: {len(fpl_data)}')
    print(f'Scout length: {len(scout_data)}')
