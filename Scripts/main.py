import streamlit as st
import joblib
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Coffee Recommender", page_icon="☕")

st.markdown("""
<style>
  .coffee-card {
    background: #EFE4CC;
    border: 1.5px solid #C9A97A;
    border-radius: 8px;
    padding: 10px 16px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .coffee-card .score {
    color: #7B4A2A;
    font-weight: bold;
    white-space: nowrap;
    margin-left: 16px;
  }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    preprocessor = joblib.load('data/preprocessor.joblib')
    weight_vector = joblib.load('data/weight_vector.joblib')
    X             = joblib.load('data/feature_matrix.joblib')
    df            = pd.read_csv('data/coffee_names.csv', index_col=0).reset_index(drop=True)
    return preprocessor, weight_vector, X, df


preprocessor, weight_vector, X, df = load_model()

st.title('☕ Coffee Recommender')

selected = st.selectbox('Search for a coffee', df['name'].tolist())

if selected:
    pos = df.index[df['name'] == selected][0]
    sims = cosine_similarity(X[pos:pos+1], X)[0]
    top_indices = [i for i in sims.argsort()[::-1] if i != pos][:5]

    st.subheader(f'Similar to: {selected}')
    for rank, i in enumerate(top_indices, 1):
        name = df['name'].iloc[i]
        score = sims[i]
        st.markdown(
            f'<div class="coffee-card">'
            f'<span>{rank}. {name}</span>'
            f'<span class="score">{score:.2f}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )
