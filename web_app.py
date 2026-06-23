import streamlit as st
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from data_processor import load_and_clean_data, normalize_features
from engine import get_recommendations

st.set_page_config(page_title="Musical Insights Engine", page_icon="🎵", layout="centered")

st.title(" Musical Insights AI Engine")
st.markdown("Build a custom mini-playlist, weight your favs, and give the recommended songs a try!")

@st.cache_data
def get_cached_data():
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'dataset.csv')
    df_orig = load_and_clean_data(data_path)
    df_scale = normalize_features(df_orig)
    return df_orig, df_scale

with st.spinner("Analyzing the music universe (81,000+ tracks)..."):
    df_original, df_scaled = get_cached_data()

#st.success("Music Universe Loaded Successfully!")

st.header("Step 1: Define Your Taste Profile")

df_original['dropdown_label'] = df_original['track_name'] + " - By: " + df_original['artists']
all_songs = sorted(df_original['dropdown_label'].unique())

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Track 1")
    song_1 = st.selectbox("Choose first song", options=["Select a song..."] + all_songs, key="s1")
    weight_1 = st.slider("Love Rating (Track 1)", 1, 5, 3, key="w1")

with col2:
    st.subheader("Track 2")
    song_2 = st.selectbox("Choose first song", options=["Select a song..."] + all_songs, key="s2")
    weight_2 = st.slider("Love Rating (Track 2)", 1, 5, 3, key="w2")

with col3:
    st.subheader("Track 3")
    song_3 = st.selectbox("Choose third song", options=["Select a song..."] + all_songs, key="s3")
    weight_3 = st.slider("Love Rating (Track 3)", 1, 5, 3, key="w3")
    
st.write("---")
st.header("Step 2: Generate Recommendations")

if song_1 != "Select a song..." and song_2 != "Select a song..." and song_3 != "Select a song...":

    if st.button("Calculate Best Vibe Matches", use_container_width=True):
        
        idx_1 = df_original[df_original['dropdown_label'] == song_1].index[0]
        idx_2 = df_original[df_original['dropdown_label'] == song_2].index[0]
        idx_3 = df_original[df_original['dropdown_label'] == song_3].index[0]

        user_indicies = [idx_1, idx_2, idx_3]
        user_weights = [float(weight_1), float(weight_2), float(weight_3)]

        with st.spinner("Finding song recommendations..."):
            recommendations = get_recommendations(df_original, df_scaled, user_indicies, user_weights, top_k=5)

        st.success("Search complete! Here are are your recommendations:")
        for idx, row in recommendations.iterrows():
            with st.container(border=True):

                text_col , tag_col = st.columns([4,1])

                with text_col:
                    st.markdown(f"### **{row['track_name']}**")
                    st.markdown(f" *{row['artists']}*")
                with tag_col:
                    st.button(f" {row['track_genre'].upper()}", disabled=True, key=f"btn_{idx}")
else:
    st.info(" Please select all 3 tracks in the columns above to activate the engine.")