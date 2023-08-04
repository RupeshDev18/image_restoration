import pickle

model_pkl_file="models/my_model.pkl"

with open(model_pkl_file, 'rb') as file:
     model = pickle.load(file)