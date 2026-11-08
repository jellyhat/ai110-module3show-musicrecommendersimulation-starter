import csv
import math
from typing import List, Dict, Tuple
from dataclasses import dataclass

# Points available for each feature when it fully matches the user's preference
WEIGHTS = {
    "genre": 1.5,
    "energy": 1.5,
    "mood": 1.0,
    "valence": 1.0,
    "acoustic": 0.5,
    "instrumental": 0.5,
}
PARTIAL_GENRE_CREDIT = 0.5  # e.g. "pop" inside "indie pop"
ENERGY_SIGMA = 0.15
VALENCE_SIGMA = 0.20
MIN_SCORE_FRACTION = 0.45  # drop songs earning less than this share of the best possible score
UNMET_FRACTION = 0.5  # a preference is unmet when a song earns less than this share of its points

# Which feature weight each user_prefs key unlocks
PREF_FEATURES = {
    "genres": "genre",
    "genre": "genre",
    "mood": "mood",
    "energy": "energy",
    "valence": "valence",
    "likes_acoustic": "acoustic",
    "likes_instrumental": "instrumental",
}

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
    instrumentalness: float

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
    likes_instrumental: bool

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
    """Read songs.csv into a list of dicts with numeric fields converted to int/float."""
    float_fields = ["energy", "tempo_bpm", "valence", "danceability", "acousticness", "instrumentalness"]

    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["id"] = int(row["id"])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)
    return songs

def normalize(text: str) -> str:
    """Lowercase and trim a label so "Pop " and "pop" compare equal."""
    return text.strip().lower()

def feature_points(user_prefs: Dict, song: Dict) -> List[Tuple[str, float, str]]:
    """Return (feature, points, reason) for every preference the user specified."""
    results = []

    # Accept a single "genre" string or a "genres" list
    genres = user_prefs.get("genres") or ([user_prefs["genre"]] if "genre" in user_prefs else [])
    genres = [normalize(g) for g in genres]
    if genres:
        song_genre = normalize(song["genre"])
        if song_genre in genres:
            results.append(("genre", WEIGHTS["genre"], f"genre match ({song['genre']})"))
        elif any(g in song_genre for g in genres):
            results.append(("genre", WEIGHTS["genre"] * PARTIAL_GENRE_CREDIT, f"partial genre match ({song['genre']})"))
        else:
            results.append(("genre", 0.0, f"genre {song['genre']} not a favorite"))

    if "mood" in user_prefs:
        matched = normalize(song["mood"]) == normalize(user_prefs["mood"])
        results.append(("mood", WEIGHTS["mood"] if matched else 0.0, f"mood match ({song['mood']})"))

    if "energy" in user_prefs:
        sim = gaussian_similarity(song["energy"], user_prefs["energy"], ENERGY_SIGMA)
        results.append(("energy", WEIGHTS["energy"] * sim, f"energy {song['energy']:.2f} vs target {user_prefs['energy']:.2f}"))

    if "valence" in user_prefs:
        sim = gaussian_similarity(song["valence"], user_prefs["valence"], VALENCE_SIGMA)
        results.append(("valence", WEIGHTS["valence"] * sim, f"valence {song['valence']:.2f} vs target {user_prefs['valence']:.2f}"))

    if "likes_acoustic" in user_prefs:
        a = song["acousticness"]
        sim = a if user_prefs["likes_acoustic"] else 1 - a
        label = "acoustic" if user_prefs["likes_acoustic"] else "non-acoustic"
        results.append(("acoustic", WEIGHTS["acoustic"] * sim, f"acousticness {a:.2f} fits {label} preference"))

    if "likes_instrumental" in user_prefs:
        i = song["instrumentalness"]
        sim = i if user_prefs["likes_instrumental"] else 1 - i
        label = "instrumental" if user_prefs["likes_instrumental"] else "vocal"
        results.append(("instrumental", WEIGHTS["instrumental"] * sim, f"instrumentalness {i:.2f} fits {label} preference"))

    return results

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Return a song's total points against user_prefs and a list of reasons showing each feature's points."""
    points = feature_points(user_prefs, song)
    score = sum(p for _, p, _ in points)
    reasons = [f"{reason} (+{p:.2f})" for _, p, reason in points if round(p, 2) > 0]
    return score, reasons

def max_possible_score(user_prefs: Dict) -> float:
    """Return the points a perfect song would earn for the preferences this user specified."""
    features = {PREF_FEATURES[key] for key, value in user_prefs.items() if key in PREF_FEATURES and value != []}
    return sum(WEIGHTS[f] for f in features)

def find_unmet_preferences(user_prefs: Dict, song: Dict) -> List[str]:
    """Return the features where a song earns less than half of the available points."""
    return [feature for feature, p, _ in feature_points(user_prefs, song) if p < WEIGHTS[feature] * UNMET_FRACTION]

def gaussian_similarity(value: float, target: float, sigma: float) -> float:
    """Return 1.0 when value equals target, falling toward 0 along a bell curve as they move apart."""
    return math.exp(-((value - target) ** 2) / (2 * sigma ** 2))

def recommend_songs(
    user_prefs: Dict, songs: List[Dict], k: int = 5, min_score_fraction: float = MIN_SCORE_FRACTION
) -> List[Tuple[Dict, float, str]]:
    """Score every song and return up to k good-enough matches as (song, score, explanation), highest first."""
    # Judge every song, then rank: highest score first, ties broken by id
    ranked = sorted(
        ((song, *score_song(user_prefs, song)) for song in songs),
        key=lambda item: (-item[1], item[0]["id"]),
    )
    # Drop weak matches so songs that fit only one preference don't fill the list
    floor = max_possible_score(user_prefs) * min_score_fraction
    good = [(song, score, "; ".join(reasons)) for song, score, reasons in ranked if score >= floor]
    return good[:k]
