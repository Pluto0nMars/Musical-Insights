import sys
import os
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_processor import load_and_clean_data, normalize_features
from engine import get_recommendations

app = Flask(__name__)
CORS(app)

current_folder = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_folder)
data_path = os.path.join(project_root, 'data', 'dataset.csv')

print("Loading songs for music database...")
df_original = load_and_clean_data(data_path)
df_scaled = normalize_features(df_original)
print(f"Loaded {len(df_original)} songs successfully!\n")



def format_duration(ms):
    try:
        total_seconds = int(ms) // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes}:{seconds:02d}"
    except (ValueError, TypeError):
        return "3:45"  
    

@app.route('/api/search', methods=['GET'])
def searchTracks():
    query = request.args.get('q', '').strip().lower()
    if not query or len(query) < 2:
        return jsonify([])

    matches = df_original[df_original['track_name'].str.lower().str.contains(query, na=False)]

    unique_matches = matches[['track_name', 'artists']].drop_duplicates(subset=['track_name']).head(10)

    results = []
    #clean_results = []

    for _, row in unique_matches.iterrows():
        results.append({
            "title":row['track_name'],
            "artist":row['artists']
        })
    return jsonify(results)

@app.route('/api/recommend', methods=['POST'])
def recommend():
    try:
        data = request.get_json()
        print("Received request from web app:", data)

        selected_tracks = data.get('tracks',[])
        selected_weights = data.get('weights', [3,3,3])

        user_playlist_indices = []
        user_playlist_weights = []

        for idx, track_name in enumerate(selected_tracks):
            matches = df_original[df_original['track_name'].str.lower() == track_name.lower()]

            if not matches.empty:
                matched_index = int(matches.index.tolist()[0])
                user_playlist_indices.append(matched_index)

                weight = selected_weights[idx] if idx < len(selected_weights) else 3
                user_playlist_weights.append(weight)

        if not user_playlist_indices:
            return jsonify({
                "success": False, 
                "message": "None of the selected tracks were found in the database."
            }),400
        
        # weights_array = np.array(user_playlist_weights)

        recommendations = get_recommendations(
            df_original,
            df_scaled,
            user_playlist_indices,
            weights=user_playlist_weights,
            top_k=5
        )

        results = []
        for _, row in recommendations.iterrows():

            raw_duration_ms = row.get('duration_ms', 0)

            results.append({
                "title": row.get('track_name', 'Unknown Title'),
                "artist": row.get('artists', 'Unknown Artist'),
                "album": row.get('album_name', 'Single'),
                "duration": format_duration(raw_duration_ms),
                "genre": row.get('track_genre', 'General')
            })
        return jsonify({"success":True, "results": results})
    
    except Exception as e:
        print("Error during recommendation:", e)
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)