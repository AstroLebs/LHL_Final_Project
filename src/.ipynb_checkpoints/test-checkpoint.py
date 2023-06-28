from modules import data_collection
import pickle

file_path = '../Data/data.pickle'

with open(file_path, 'rb') as f:
    data = pickle.load(f)
