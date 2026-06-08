"""
Command line runner for the Music Recommender Simulation.

Run from the project root:
    python -m src.main
"""

from .recommender import load_songs, recommend_songs


PROFILES = [
    ("Happy Pop Fan",       {"genre": "pop",     "mood": "happy",       "energy": 0.80}),
    ("Chill Lofi Studier",  {"genre": "lofi",    "mood": "chill",       "energy": 0.40}),
    ("High-Energy EDM",     {"genre": "edm",     "mood": "euphoric",    "energy": 0.95}),
    ("Deep Blues Listener", {"genre": "blues",   "mood": "melancholic", "energy": 0.45}),
    ("Intense Metalhead",   {"genre": "metal",   "mood": "intense",     "energy": 0.95}),
]


def print_profile_recs(label: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Print a formatted recommendation block for one user profile."""
    print(f"\n{'=' * 52}")
    print(f"Profile : {label}")
    print(f"Prefs   : genre={user_prefs['genre']}, mood={user_prefs['mood']}, energy={user_prefs['energy']}")
    print(f"{'=' * 52}")
    for i, (song, score, explanation) in enumerate(recommend_songs(user_prefs, songs, k=k), 1):
        print(f"  {i}. {song['title']} — {song['artist']}")
        print(f"     Score: {score:.2f}  |  {explanation}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for label, prefs in PROFILES:
        print_profile_recs(label, prefs, songs)


if __name__ == "__main__":
    main()
