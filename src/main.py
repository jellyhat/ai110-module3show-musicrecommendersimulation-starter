"""
Command line runner for the Music Recommender Simulation.
"""

from src.recommender import find_unmet_preferences, load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    profiles = {
        # Upbeat listener: pop and rock fan who wants happy, high energy songs
        "Upbeat Pop/Rock": {
            "genres": ["pop", "rock"],
            "mood": "happy",
            "energy": 0.85,
            "valence": 0.8,
        },
        # Edge case: conflicting preferences. The only "sad" song in the
        # catalog is low energy, so mood and energy pull in opposite directions
        "Sad but Energetic": {
            "mood": "sad",
            "energy": 0.9,
            "valence": 0.2,
        },
        # Edge case: impossible combination. Every EDM track is electronic,
        # so the genre and acoustic preferences can't both be satisfied
        "Acoustic EDM Fan": {
            "genres": ["edm"],
            "mood": "euphoric",
            "energy": 0.95,
            "likes_acoustic": True,
        },
        # Edge case: same taste as Upbeat Pop/Rock, but typed with capital
        # letters. Tests whether genre and mood matching is case-sensitive
        "Capitalized Input": {
            "genres": ["Pop", "Rock"],
            "mood": "Happy",
            "energy": 0.85,
            "valence": 0.8,
        },
    }

    for name, user_prefs in profiles.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print(f"\n=== {name} ===")
        print(f"Preferences: {user_prefs}\n")

        if not recommendations:
            print("No songs matched these preferences closely enough.\n")
            continue
        if len(recommendations) < 5:
            print(f"Only {len(recommendations)} song(s) matched closely enough.")
        unmet = find_unmet_preferences(user_prefs, recommendations[0][0])
        if unmet:
            print(f"Heads up: even the top match falls short on: {', '.join(unmet)}.")
            print("Some of these preferences may conflict with each other.\n")

        for song, score, explanation in recommendations:
            print(f"{song['title']} ({song['genre']}, {song['mood']}) - Score: {score:.2f}")
            print(f"Because: {explanation}")
            print()


if __name__ == "__main__":
    main()
