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


    candidate_pool = top_k * 6
    top_candidate_indicies = np.argsort(scores_filtered)[-candidate_pool:][::-1]

    diverse_indicies = []
    seen_artists =  set()

    for idx in top_candidate_indicies:
        artist = df_original.loc[idx, 'artists']

        if artist not in seen_artists:
            diverse_indicies.append(idx)
            seen_artists.add(artist)

        if len(diverse_indicies) == top_k:
            break


    if len(diverse_indicies) < top_k:
        for idx in top_candidate_indicies:
            if idx not in diverse_indicies:
                diverse_indicies.append(idx)
            if len(diverse_indicies) == top_k:
                break

    return df_original.iloc[diverse_indicies]


