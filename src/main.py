"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from src.recommender import load_songs, recommend_songs, MAX_SCORE  # python -m src.main
except ImportError:
    from recommender import load_songs, recommend_songs, MAX_SCORE  # python src/main.py


PROFILES = {
    # --- Distinct, realistic taste profiles ---
    "High-Energy Pop": {
        "favorite_genre": "pop", "favorite_mood": "happy",
        "target_energy": 0.80, "target_valence": 0.80, "likes_acoustic": False,
    },
    "Chill Lofi": {
        "favorite_genre": "lofi", "favorite_mood": "chill",
        "target_energy": 0.40, "target_valence": 0.60, "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock", "favorite_mood": "intense",
        "target_energy": 0.92, "target_valence": 0.45, "likes_acoustic": False,
    },
    # --- Adversarial / edge-case profiles ---
    "ADVERSARIAL: Sad but Energetic": {  # mood and energy pull in opposite directions
        "favorite_genre": "folk", "favorite_mood": "melancholic",
        "target_energy": 0.90, "target_valence": 0.20, "likes_acoustic": False,
    },
    "ADVERSARIAL: Acoustic Metalhead": {  # metal is never acoustic in this catalog
        "favorite_genre": "metal", "favorite_mood": "aggressive",
        "target_energy": 0.97, "target_valence": 0.22, "likes_acoustic": True,
    },
    "ADVERSARIAL: Unknown Genre and Mood": {  # labels that match no song at all
        "favorite_genre": "bossa nova", "favorite_mood": "dreamy",
        "target_energy": 0.50, "target_valence": 0.70, "likes_acoustic": True,
    },
    "ADVERSARIAL: Dead Center": {  # every target in the middle of the range
        "favorite_genre": "pop", "favorite_mood": "happy",
        "target_energy": 0.50, "target_valence": 0.50, "likes_acoustic": False,
    },
}


def print_recommendations(name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Run the recommender for one profile and print a formatted top-k list."""
    recommendations = recommend_songs(user_prefs, songs, k=k)

    width = 64
    print("\n" + "=" * width)
    print(f"PROFILE: {name}")
    print(
        f"genre={user_prefs['favorite_genre']}, mood={user_prefs['favorite_mood']}, "
        f"energy={user_prefs['target_energy']}, valence={user_prefs['target_valence']}, "
        f"likes_acoustic={user_prefs['likes_acoustic']}"
    )
    print(f"Top {len(recommendations)} recommendations")
    print("=" * width)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{rank}  {song['title']} by {song['artist']} [{song['genre']}/{song['mood']}]")
        print(f"    Score: {score:.2f} / {MAX_SCORE:.2f}")
        print("    Reasons:")
        for reason in explanation.split("; "):
            print(f"      - {reason}")


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for name, user_prefs in PROFILES.items():
        print_recommendations(name, user_prefs, songs)


if __name__ == "__main__":
    main()
