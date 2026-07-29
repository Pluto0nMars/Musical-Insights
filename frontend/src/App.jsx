import React, { useState } from 'react';
import { Music4, Disc3, SlidersHorizontal, Sparkles } from 'lucide-react';
import RecommendationCard from './components/RecommendationCard';

export default function App() {
  // React State for selected songs and ratings
  const [tracks, setTracks] = useState([
    { id: 1, title: "Island In The Sun", weight: 5 },
    { id: 2, title: "Say It Ain't So", weight: 4 },
    { id: 3, title: "", weight: 3 }
  ]);

  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Helper to handle updating track titles
  const handleTrackChange = (index, value) => {
    const updated = [...tracks];
    updated[index].title = value;
    setTracks(updated);
  };

  // Helper to handle slider rating updates
  const handleWeightChange = (index, value) => {
    const updated = [...tracks];
    updated[index].weight = parseFloat(value);
    setTracks(updated);
  };

  return (
    <div className="app-container">
      <header>
        <Music4 size={32} />
        <h1>Musical Insights AI</h1>
        <p class="subtitle">React Dashboard</p>
      </header>

     
      <section className="step-section">
        <h2>Step 1: Define your song Profile</h2>
        <div className="selector-grid">
          {tracks.map((track, idx) => (
            <div key={track.id} className="track-card">
              <Disc3 size={24} />
              <h3>Track {idx + 1}</h3>

              <select 
                className="track-select"
                value={track.title}
                onChange={(e) => handleTrackChange(idx, e.target.value)}
              >
                <option value="">Choose a song...</option>
                <option value="Island In The Sun">Island In The Sun - By: Weezer</option>
                <option value="Say It Ain't So">Say It Ain't So - By: Weezer</option>
                <option value="I'll Be Back!">I'll Be Back! - By: Rilès</option>
              </select>

              <div className="slider-container">
                <label>
                  <SlidersHorizontal size={14} />
                  Love Rating: <span className="weight-val">{track.weight}</span>
                </label>
                <input 
                  type="range" 
                  className="track-weight" 
                  min="1" 
                  max="5" 
                  value={track.weight}
                  onChange={(e) => handleWeightChange(idx, e.target.value)}
                />
              </div>
            </div>
          ))}
        </div>
      </section>

      
      <section className="step-section">
        <h2>Step 2: Generate Recommendations</h2>
        <button className="btn-submit" id="generate-btn">
          <Sparkles size={18} />
          Generate Best Vibe Matches
        </button>
      </section>

     
      {recommendations.length > 0 && (
        <section className="results-container">
          <h2>Your Curated Matches</h2>
          <div className="results-grid">
            {recommendations.map((song, index) => (
              <RecommendationCard key={index} song={song} rank={index + 1} />
            ))}
          </div>
        </section>
      )}
    </div>
  );
}