from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from data_processor import load_and_clean_data, normalize_features
from engine import get_recommendations

app = Flask(__name__)
CORS(app)

print("Initializing Music AI Brain...")
data_path = os.path.join(os.path.dirname(__file__), 'data', 'dataset.csv')
df_original = load_and_clean_data(data_path)
df_scale = normalize_features(df_original)

df_original['dropdown_label'] = df_original['track_name']+ " - By: " + df_original['artists']
print("Music Database Loaded!")

@app.route('/api/songs', methods=['GET'])
def get_all_songs():
    """returns a list of all songs to display in search boxes."""
    song_list = sorted(df_original['dropdown_label'].unique().tolist())
    return jsonify(song_list)

@app.route('/api/recommend', methods=['POST'])
def recommend():
    """Receives selected songs and weights from React, runs math, returns top 5."""
    data = request.join

    selected_labels = data.get('songs', [])
    weights = data.get('weights', [])


    if len(selected_labels) < 3:
        return jsonify({"error":"Please provide exactly 3 songs"}) , 400
    
    try:

        user_indicies = []
        for label in selected_labels:
            idx = df_original[df_original['dropdown_label'] == label].index[0]
            user_indicies.append(int(idx))

        recommendaations = get_recommendations(df_original, df_scale, user_indicies, weights, top_k=5)

        results = []

        for idx, row in recommendaations.iterrows():
            results.append({
                "track_name": row['track_name'],
                "artists": row['artists'],
                "genre": row['track_genre']
            })

        return jsonify(results)
    except  Exception as e:

        return jsonify({"error": str(e)}), 500
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,debug=True)