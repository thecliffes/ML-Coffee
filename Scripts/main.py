import joblib
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

preprocessor = joblib.load('preprocessor.joblib')
X = joblib.load('feature_matrix.joblib')
df = pd.read_csv('coffee_names.csv', index_col=0)

# weight_vector needs to be rebuilt or also saved
import numpy as np
joblib.dump(weight_vector, 'weight_vector.joblib')
weight_vector = joblib.load('weight_vector.joblib')
