import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class Song:
    """Represents a song and its attributes."""
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
    """Represents a user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """OOP recommendation engine that ranks songs against a UserProfile."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs ranked by relevance to the user profile."""
        return sorted(self.songs, key=lambda s: self._song_score(user, s), reverse=True)[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why a song was recommended."""
        reasons = []
        if song.genre == user.favorite_genre:
            reasons.append(f"genre match: {song.genre} (+2.0)")
        if song.mood == user.favorite_mood:
            reasons.append(f"mood match: {song.mood} (+1.0)")
        energy_gap = abs(user.target_energy - song.energy)
        energy_score = round(1.5 * (1.0 - energy_gap), 2)
        reasons.append(f"energy proximity (+{energy_score:.2f})")
        if user.likes_acoustic and song.acousticness > 0.6:
            reasons.append("acoustic preference (+0.5)")
        elif not user.likes_acoustic and song.acousticness < 0.4:
            reasons.append("non-acoustic preference (+0.3)")
        return ", ".join(reasons)

    def _song_score(self, user: UserProfile, song: Song) -> float:
        """Numeric score for a song given a user profile (used internally for sorting)."""
        score = 0.0
        if song.genre == user.favorite_genre:
            score += 2.0
        if song.mood == user.favorite_mood:
            score += 1.0
        energy_gap = abs(user.target_energy - song.energy)
        score += 1.5 * (1.0 - energy_gap)
        if user.likes_acoustic and song.acousticness > 0.6:
            score += 0.5
        elif not user.likes_acoustic and song.acousticness < 0.4:
            score += 0.3
        return score


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file, converting numeric fields to float/int."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song against user preferences; return (score, reasons)."""
    score = 0.0
    reasons = []

    # Genre match: +2.0 points
    if song.get("genre", "").lower() == user_prefs.get("genre", "").lower():
        score += 2.0
        reasons.append(f"genre match: {song['genre']} (+2.0)")

    # Mood match: +1.0 points
    if song.get("mood", "").lower() == user_prefs.get("mood", "").lower():
        score += 1.0
        reasons.append(f"mood match: {song['mood']} (+1.0)")

    # Energy proximity: up to +1.5 points (closer to target = more points)
    if "energy" in user_prefs:
        energy_gap = abs(float(user_prefs["energy"]) - float(song.get("energy", 0.5)))
        energy_score = round(1.5 * (1.0 - energy_gap), 2)
        score += energy_score
        reasons.append(f"energy proximity (+{energy_score:.2f})")

    # Valence proximity: up to +0.5 points (optional preference)
    if "valence" in user_prefs:
        valence_gap = abs(float(user_prefs["valence"]) - float(song.get("valence", 0.5)))
        valence_score = round(0.5 * (1.0 - valence_gap), 2)
        score += valence_score
        reasons.append(f"valence proximity (+{valence_score:.2f})")

    return round(score, 2), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score and rank all songs; return the top k as (song, score, explanation) tuples."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons) if reasons else "no strong matches"
        scored.append((song, score, explanation))
    # sorted() returns a new list; original catalog is unchanged
    scored = sorted(scored, key=lambda x: x[1], reverse=True)
    return scored[:k]
