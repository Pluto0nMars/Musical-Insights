import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_processor import load_and_clean_data, normalize_features
from engine import get_recommendations

def main():
    current_folder = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_folder)
    data_path =  os.path.join(project_root, 'data', 'dataset.csv')

    print("Loading songs for music database")

    df_original =  load_and_clean_data(data_path)
    df_scaled =  normalize_features(df_original)

    print(f"Loaded {len(df_original)} songs successfully!\n")

    print("Let's build a mini-playlist. Type the exact names of 3 songs you like.")
    print("(Tip: If a song isn't found, we'll let you know so you can try another one!)\n")

    user_playlist_indices = []
    songs_needed = 3

    while len(user_playlist_indices) < songs_needed:
        song_input = input(f"Enter song name ({len(user_playlist_indices) + 1}/{songs_needed}): ").strip()

        matches = df_original[df_original['track_name'].str.lower() ==  song_input.lower()]

        if matches.empty:
            print(f"Couldn't find '{song_input}' in the dataset. Try another song!")
        else:
            matched_index = matches.index[0]
            track_title = df_original.loc[matched_index, 'track_name']
            artist_name = df_original.loc[matched_index, 'artists']
            user_playlist_indices.append(matched_index)
            
            print(f"  Found: '{track_title}' by {artist_name}")

    recommendations = get_recommendations(df_original, df_scaled, user_playlist_indices, top_k=5)
    

    print("\n HERE ARE YOUR 5 RECOMMENDATIONS: ")

    print("=" * 60)

    for idx, row in recommendations.iterrows():
        print(f" '{row['track_name']}' - By: {row['artists']} [{row['track_genre']}] ")

    print("=" * 60)

if __name__ == "__main__":
    main()