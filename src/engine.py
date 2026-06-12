import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

FEATURE_COLS = [
    'danceability', 'energy', 'loudness', 'speechiness', 
    'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo'
]


def create_playlist_profile(df_scaled, playlist_indices):
    playlist_features =  df_scaled.loc[playlist_indices, FEATURE_COLS]

    playlist_profile = np.mean(playlist_features, axis=0)

    return playlist_profile.values.reshape(1, -1)

def get_recommendations(df_original, df_scaled, playlist_indicies, top_k=5):

    user_profile = create_playlist_profile(df_scaled, playlist_indicies)

    all_features = df_scaled[FEATURE_COLS].values

    scores = cosine_similarity(user_profile, all_features).flatten()

    scores_filtered = scores.copy()
    scores_filtered[playlist_indicies] = -1

    top_indicies = np.argsort(scores_filtered)[-top_k:][::-1]

    return df_original.iloc[top_indicies]


