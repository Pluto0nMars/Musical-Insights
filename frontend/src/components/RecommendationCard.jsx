import React from 'react';
import { User, Library, Clock, Tag } from 'lucide-react';

export default function RecommendationCard({song, rank}){
    return (<div className="rec-card">
      <div className="track-info">
        <strong className="track-name">#{rank} {song.title}</strong>
        <div className="meta-row">
          <span className="artist-name">
            <User size={14} /> {song.artist}
          </span>
          <span className="album-name">
            <Library size={14} /> {song.album}
          </span>
          <span className="duration-text">
            <Clock size={14} /> {song.duration}
          </span>
        </div>
      </div>
      
      <div className="genre-wrapper">
        <Tag size={14} />
        <span className="genre-tag">{song.genre}</span>
      </div>
    </div>
  );
}