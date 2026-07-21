import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from CSV, converting numeric fields to floats for scoring."""
    songs = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            song = {
                'id': int(row['id']),
                'title': row['title'],
                'artist': row['artist'],
                'genre': row['genre'],
                'mood': row['mood'],
                'energy': float(row['energy']),
                'tempo_bpm': float(row['tempo_bpm']),
                'valence': float(row['valence']),
                'danceability': float(row['danceability']),
                'acousticness': float(row['acousticness']),
            }
            songs.append(song)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song against user preferences, returning (score, reasons)."""
    reasons = []

    # Genre matching (0.4 weight) — exact match or nothing
    genre_match = 1 if song['genre'] == user_prefs['genre'] else 0
    genre_score = 0.4 * genre_match
    if genre_match == 1:
        reasons.append(f"Genre match: {song['genre']} (+{genre_score:.2f})")
    else:
        reasons.append(f"Genre mismatch: {song['genre']} vs {user_prefs['genre']} (0.00)")

    # Mood matching (0.3 weight) — exact match or nothing
    mood_match = 1 if song['mood'] == user_prefs['mood'] else 0
    mood_score = 0.3 * mood_match
    if mood_match == 1:
        reasons.append(f"Mood match: {song['mood']} (+{mood_score:.2f})")
    else:
        reasons.append(f"Mood mismatch: {song['mood']} vs {user_prefs['mood']} (0.00)")

    # Energy closeness (0.2 weight) — 1 - |diff|
    energy_diff = abs(song['energy'] - user_prefs['energy'])
    energy_score = 0.2 * (1 - energy_diff)
    reasons.append(f"Energy closeness: {song['energy']:.2f} vs target {user_prefs['energy']:.2f} (+{energy_score:.2f})")

    # Acoustic preference (0.1 weight)
    likes_acoustic = user_prefs.get('likes_acoustic', False)
    if likes_acoustic:
        acoustic_score = 0.1 * song['acousticness']
        reasons.append(f"High acousticness: {song['acousticness']:.2f} (+{acoustic_score:.2f})")
    else:
        acoustic_score = 0.1 * (1 - song['acousticness'])
        reasons.append(f"Low acousticness preference: {song['acousticness']:.2f} (+{acoustic_score:.2f})")

    total_score = genre_score + mood_score + energy_score + acoustic_score

    return (total_score, reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score all songs and return top k recommendations sorted by score."""
    # Score all songs and format explanations in one pass (Pythonic list comprehension)
    scored = [(song, score, ' | '.join(reasons))
              for song in songs
              for score, reasons in [score_song(user_prefs, song)]]

    # Sort by score descending, return top k
    return sorted(scored, key=lambda x: x[1], reverse=True)[:k]
