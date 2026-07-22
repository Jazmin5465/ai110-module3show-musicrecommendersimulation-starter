"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded {len(songs)} songs from CSV\n")

    # Adversarial/Edge Case Profiles
    test_profiles = [
        {
            "name": "[1] CONFLICTING: High Energy + Sad Mood",
            "prefs": {"genre": "pop", "mood": "sad", "energy": 0.9, "likes_acoustic": False},
            "reason": "Typically sad songs are low energy—how does the recommender handle this conflict?"
        },
        {
            "name": "[2] EXTREME: Maximum Energy (1.0) + Acoustic Preference",
            "prefs": {"genre": "rock", "mood": "happy", "energy": 1.0, "likes_acoustic": True},
            "reason": "Acoustic songs rarely have extreme energy. Will it struggle?"
        },
        {
            "name": "[3] EXTREME: Minimum Energy (0.0) + Danceability Preference",
            "prefs": {"genre": "jazz", "mood": "calm", "energy": 0.0, "likes_acoustic": False},
            "reason": "Low energy + low acoustic preference might penalize all songs."
        },
        {
            "name": "[4] RARE COMBO: Uncommon genre + mood mix",
            "prefs": {"genre": "classical", "mood": "energetic", "energy": 0.8, "likes_acoustic": True},
            "reason": "Classical + energetic might not exist. Zero genre matches?"
        },
        {
            "name": "[5] NEUTRAL PROFILE: Middle-of-the-road everything",
            "prefs": {"genre": "pop", "mood": "neutral", "energy": 0.5, "likes_acoustic": False},
            "reason": "Will all songs score similarly, making ranking unclear?"
        },
    ]

    for profile in test_profiles:
        print("=" * 70)
        print(f"PROFILE: {profile['name']}")
        print(f"Why: {profile['reason']}")
        print(f"Preferences: {profile['prefs']}")
        print("=" * 70 + "\n")

        try:
            recommendations = recommend_songs(profile['prefs'], songs, k=5)

            if not recommendations:
                print("[WARNING] NO RECOMMENDATIONS GENERATED!\n")
                continue

            for rank, rec in enumerate(recommendations, start=1):
                song, score, explanation = rec
                print(f"{rank}. {song['title']} by {song['artist']}")
                print(f"   Score: {score:.2f} | Genre: {song['genre']} | Mood: {song['mood']} | Energy: {song['energy']:.2f}")

                # Show scoring breakdown
                reasons = explanation.split(" | ")
                for reason in reasons:
                    print(f"   -> {reason}")
                print()
        except Exception as e:
            print(f"[ERROR] {e}\n")

        print()


if __name__ == "__main__":
    main()
