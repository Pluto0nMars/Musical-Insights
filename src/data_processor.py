import pandas as pd
from sklearn.preprocessing import StandardScaler

FEATURE_COlS = [
    'danceability', 'energy', 'loudness', 'speechiness', 
    'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo'
]

def load_and_clean_data(file_path):

    df = pd.read_csv(file_path)

    df =  df.dropna(subset=['track_name', 'artists'])

    df = df.drop_duplicates(subset=['track_name', 'artists'], keep='first')

    df = df.reset_index(drop=True)
    
    return df


def normalize_features(df):

    scaler = StandardScaler()

    df_scaled = df.copy()
    df_scaled[FEATURE_COlS] = scaler.fit_transform(df[FEATURE_COlS])

    return df_scaled