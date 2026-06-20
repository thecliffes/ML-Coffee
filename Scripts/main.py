import joblib
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

preprocessor = joblib.load('data/preprocessor.joblib')
print("Preprocessor loaded successfully.")
weight_vector = joblib.load('data/weight_vector.joblib')
print("Weight vector loaded successfully.")
X = joblib.load('data/feature_matrix.joblib')
df = pd.read_csv('data/coffee_names.csv', index_col=0)
print("Data loaded successfully.")

# weight_vector needs to be rebuilt or also saved
import numpy as np
joblib.dump(weight_vector, 'data/weight_vector.joblib')
weight_vector = joblib.load('data/weight_vector.joblib')
print("Weight vector rebuilt and loaded successfully.")


