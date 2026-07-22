# 🎵 Music Recommender Simulation

## Project Summary

This is a music recommender that scores songs based on user preferences for genre, mood, energy level, and acoustic sound. It then returns the top 5 matches ranked by score and a short explanation.

The system was stress-tested with 5 unique user profiles designed to expose edge cases: conflicting preferences (high energy + sad mood), contradictory preferences (max energy + acoustic instruments), extreme values (energy 0.0 or 1.0), rare combinations that don't exist in the dataset (classical + energetic), and impossible preferences (neutral mood). Through testing and experimentation with weight adjustments, the project demonstrates how small changes to scoring priorities completely change which songs rank first, how dataset imbalance creates systemic bias (popular genres get more matches), and how recommenders are fundamentally math and design choices rather than objective truth.

---

## How The System Works

Real-world recommenders like Spotify or YouTube blend two main strategies: collaborative filtering, which predicts what a listener will like based on the behavior of other users with similar taste, and content-based filtering, which matches a song's own attributes (genre, tempo, mood) against a listener's known preferences. Production systems combine both, plus signals like NLP-mined cultural context, so they can recommend brand-new songs with no listening history yet as well as songs backed by strong social proof. Our simulation implements only the content-based half: each `Song` carries genre, mood, energy, tempo_bpm, valence, danceability, and acousticness, and each `UserProfile` stores a single listener's favorite_genre, favorite_mood, target_energy, and likes_acoustic preference. The `Recommender` scores every song by combining a categorical match on mood (0.3 weight), a numeric closeness score on energy (0.4 weight, the highest priority) computed as `1 - |song_energy - target_energy|` so songs are rewarded for feeling the way the user wants, a genre match (0.2 weight), and an acoustic preference bonus (0.1 weight). This weighting prioritizes how a song feels (energy and mood) over what it's labeled as (genre). Songs are then ranked by total score and the top `k` are returned as recommendations. Because there's no data on other listeners, our system can't yet capture "people like you also liked" style discovery unlike real platforms that use collaborative filtering to introduce discovery. This recommender will always lean toward recommending more of what a user already says they like.

**Scoring Formula:**

```
total_score = (0.2 × genre_match) + (0.3 × mood_match) + (0.4 × energy_score) + (0.1 × acoustic_score)

where:
  genre_match    = 1 if song.genre == profile.favorite_genre else 0
  mood_match     = 1 if song.mood == profile.favorite_mood else 0
  energy_score   = 1 - |song.energy - profile.target_energy|
  acoustic_score = (1 - song.acousticness) if not profile.likes_acoustic else song.acousticness
```

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Stress Testing: Adversarial Profiles

Testing the recommender's robustness with conflicting, extreme, and edge-case user preferences:

### Profile 1: CONFLICTING — High Energy + Sad Mood

```text
PROFILE: [1] CONFLICTING: High Energy + Sad Mood
Why: Typically sad songs are low energy—how does the recommender handle this conflict?
Preferences: {'genre': 'pop', 'mood': 'sad', 'energy': 0.9, 'likes_acoustic': False}

1. Gym Hero by Max Pulse
   Score: 0.69 | Genre: pop | Mood: intense | Energy: 0.93
   -> Genre match: pop (+0.40)
   -> Mood mismatch: intense vs sad (0.00)
   -> Energy closeness: 0.93 vs target 0.90 (+0.19)
   -> Low acousticness preference: 0.05 (+0.10)

2. Sunrise City by Neon Echo
   Score: 0.67 | Genre: pop | Mood: happy | Energy: 0.82
   -> Genre match: pop (+0.40)
   -> Mood mismatch: happy vs sad (0.00)
   -> Energy closeness: 0.82 vs target 0.90 (+0.18)
   -> Low acousticness preference: 0.18 (+0.08)

3. Storm Runner by Voltline
   Score: 0.29 | Genre: rock | Mood: intense | Energy: 0.91
   -> Genre mismatch: rock vs pop (0.00)
   -> Mood mismatch: intense vs sad (0.00)
   -> Energy closeness: 0.91 vs target 0.90 (+0.20)
   -> Low acousticness preference: 0.10 (+0.09)

4. Neon Dreams by Volt Surge
   Score: 0.28 | Genre: electronic | Mood: energetic | Energy: 0.88
   -> Genre mismatch: electronic vs pop (0.00)
   -> Mood mismatch: energetic vs sad (0.00)
   -> Energy closeness: 0.88 vs target 0.90 (+0.20)
   -> Low acousticness preference: 0.12 (+0.09)

5. Thunder by Metal Storm
   Score: 0.28 | Genre: metal | Mood: aggressive | Energy: 0.94
   -> Genre mismatch: metal vs pop (0.00)
   -> Mood mismatch: aggressive vs sad (0.00)
   -> Energy closeness: 0.94 vs target 0.90 (+0.19)
   -> Low acousticness preference: 0.08 (+0.09)
```

### Profile 2: EXTREME — Maximum Energy (1.0) + Acoustic Preference

```text
PROFILE: [2] EXTREME: Maximum Energy (1.0) + Acoustic Preference
Why: Acoustic songs rarely have extreme energy. Will it struggle?
Preferences: {'genre': 'rock', 'mood': 'happy', 'energy': 1.0, 'likes_acoustic': True}

1. Storm Runner by Voltline
   Score: 0.59 | Genre: rock | Mood: intense | Energy: 0.91
   -> Genre match: rock (+0.40)
   -> Mood mismatch: intense vs happy (0.00)
   -> Energy closeness: 0.91 vs target 1.00 (+0.18)
   -> High acousticness: 0.10 (+0.01)

2. Rooftop Lights by Indigo Parade
   Score: 0.49 | Genre: indie pop | Mood: happy | Energy: 0.76
   -> Genre mismatch: indie pop vs rock (0.00)
   -> Mood match: happy (+0.30)
   -> Energy closeness: 0.76 vs target 1.00 (+0.15)
   -> High acousticness: 0.35 (+0.03)

3. Sunrise City by Neon Echo
   Score: 0.48 | Genre: pop | Mood: happy | Energy: 0.82
   -> Genre mismatch: pop vs rock (0.00)
   -> Mood match: happy (+0.30)
   -> Energy closeness: 0.82 vs target 1.00 (+0.16)
   -> High acousticness: 0.18 (+0.02)

4. Thunder by Metal Storm
   Score: 0.20 | Genre: metal | Mood: aggressive | Energy: 0.94
   -> Genre mismatch: metal vs rock (0.00)
   -> Mood mismatch: aggressive vs happy (0.00)
   -> Energy closeness: 0.94 vs target 1.00 (+0.19)
   -> High acousticness: 0.08 (+0.01)

5. Gym Hero by Max Pulse
   Score: 0.19 | Genre: pop | Mood: intense | Energy: 0.93
   -> Genre mismatch: pop vs rock (0.00)
   -> Mood mismatch: intense vs happy (0.00)
   -> Energy closeness: 0.93 vs target 1.00 (+0.19)
   -> High acousticness: 0.05 (+0.01)
```

### Profile 3: EXTREME — Minimum Energy (0.0) + Low Acoustic Preference

```text
PROFILE: [3] EXTREME: Minimum Energy (0.0) + Danceability Preference
Why: Low energy + low acoustic preference might penalize all songs.
Preferences: {'genre': 'jazz', 'mood': 'calm', 'energy': 0.0, 'likes_acoustic': False}

1. Coffee Shop Stories by Slow Stereo
   Score: 0.54 | Genre: jazz | Mood: relaxed | Energy: 0.37
   -> Genre match: jazz (+0.40)
   -> Mood mismatch: relaxed vs calm (0.00)
   -> Energy closeness: 0.37 vs target 0.00 (+0.13)
   -> Low acousticness preference: 0.89 (+0.01)

2. Moonlight Sonata by Symphony Strings
   Score: 0.16 | Genre: classical | Mood: peaceful | Energy: 0.25
   -> Genre mismatch: classical vs jazz (0.00)
   -> Mood mismatch: peaceful vs calm (0.00)
   -> Energy closeness: 0.25 vs target 0.00 (+0.15)
   -> Low acousticness preference: 0.94 (+0.01)

3. Spacewalk Thoughts by Orbit Bloom
   Score: 0.15 | Genre: ambient | Mood: chill | Energy: 0.28
   -> Genre mismatch: ambient vs jazz (0.00)
   -> Mood mismatch: chill vs calm (0.00)
   -> Energy closeness: 0.28 vs target 0.00 (+0.14)
   -> Low acousticness preference: 0.92 (+0.01)

4. Morning Mist by Acoustic Wanderer
   Score: 0.15 | Genre: folk | Mood: nostalgic | Energy: 0.32
   -> Genre mismatch: folk vs jazz (0.00)
   -> Mood mismatch: nostalgic vs calm (0.00)
   -> Energy closeness: 0.32 vs target 0.00 (+0.14)
   -> Low acousticness preference: 0.88 (+0.01)

5. Midnight Coding by LoRoom
   Score: 0.15 | Genre: lofi | Mood: chill | Energy: 0.42
   -> Genre mismatch: lofi vs jazz (0.00)
   -> Mood mismatch: chill vs calm (0.00)
   -> Energy closeness: 0.42 vs target 0.00 (+0.12)
   -> Low acousticness preference: 0.71 (+0.03)
```

### Profile 4: RARE COMBO — Classical + Energetic (Mismatched Mood & Energy)

```text
PROFILE: [4] RARE COMBO: Uncommon genre + mood mix
Why: Classical + energetic might not exist. Zero genre matches?
Preferences: {'genre': 'classical', 'mood': 'energetic', 'energy': 0.8, 'likes_acoustic': True}

1. Moonlight Sonata by Symphony Strings
   Score: 0.58 | Genre: classical | Mood: peaceful | Energy: 0.25
   -> Genre match: classical (+0.40)
   -> Mood mismatch: peaceful vs energetic (0.00)
   -> Energy closeness: 0.25 vs target 0.80 (+0.09)
   -> High acousticness: 0.94 (+0.09)

2. Neon Dreams by Volt Surge
   Score: 0.50 | Genre: electronic | Mood: energetic | Energy: 0.88
   -> Genre mismatch: electronic vs classical (0.00)
   -> Mood match: energetic (+0.30)
   -> Energy closeness: 0.88 vs target 0.80 (+0.18)
   -> High acousticness: 0.12 (+0.01)

3. Rooftop Lights by Indigo Parade
   Score: 0.23 | Genre: indie pop | Mood: happy | Energy: 0.76
   -> Genre mismatch: indie pop vs classical (0.00)
   -> Mood mismatch: happy vs energetic (0.00)
   -> Energy closeness: 0.76 vs target 0.80 (+0.19)
   -> High acousticness: 0.35 (+0.03)

4. Sunrise City by Neon Echo
   Score: 0.21 | Genre: pop | Mood: happy | Energy: 0.82
   -> Genre mismatch: pop vs classical (0.00)
   -> Mood mismatch: happy vs energetic (0.00)
   -> Energy closeness: 0.82 vs target 0.80 (+0.20)
   -> High acousticness: 0.18 (+0.02)

5. Sunshine Reggae by Island Vibes
   Score: 0.21 | Genre: reggae | Mood: uplifting | Energy: 0.55
   -> Genre mismatch: reggae vs classical (0.00)
   -> Mood mismatch: uplifting vs energetic (0.00)
   -> Energy closeness: 0.55 vs target 0.80 (+0.15)
   -> High acousticness: 0.63 (+0.06)
```

### Profile 5: NEUTRAL — Middle-of-the-Road Everything

```text
PROFILE: [5] NEUTRAL PROFILE: Middle-of-the-road everything
Why: Will all songs score similarly, making ranking unclear?
Preferences: {'genre': 'pop', 'mood': 'neutral', 'energy': 0.5, 'likes_acoustic': False}

1. Sunrise City by Neon Echo
   Score: 0.62 | Genre: pop | Mood: happy | Energy: 0.82
   -> Genre match: pop (+0.40)
   -> Mood mismatch: happy vs neutral (0.00)
   -> Energy closeness: 0.82 vs target 0.50 (+0.14)
   -> Low acousticness preference: 0.18 (+0.08)

2. Gym Hero by Max Pulse
   Score: 0.61 | Genre: pop | Mood: intense | Energy: 0.93
   -> Genre match: pop (+0.40)
   -> Mood mismatch: intense vs neutral (0.00)
   -> Energy closeness: 0.93 vs target 0.50 (+0.11)
   -> Low acousticness preference: 0.05 (+0.10)

3. Street Poetry by Urban Echo
   Score: 0.24 | Genre: hip-hop | Mood: confident | Energy: 0.72
   -> Genre mismatch: hip-hop vs pop (0.00)
   -> Mood mismatch: confident vs neutral (0.00)
   -> Energy closeness: 0.72 vs target 0.50 (+0.16)
   -> Low acousticness preference: 0.21 (+0.08)

4. Fading Light by Dusty Roads
   Score: 0.23 | Genre: indie rock | Mood: melancholic | Energy: 0.58
   -> Genre mismatch: indie rock vs pop (0.00)
   -> Mood mismatch: melancholic vs neutral (0.00)
   -> Energy closeness: 0.58 vs target 0.50 (+0.18)
   -> Low acousticness preference: 0.52 (+0.05)

5. Velvet Nights by Smooth Soul
   Score: 0.23 | Genre: soul | Mood: romantic | Energy: 0.61
   -> Genre mismatch: soul vs pop (0.00)
   -> Mood mismatch: romantic vs neutral (0.00)
   -> Energy closeness: 0.61 vs target 0.50 (+0.18)
   -> Low acousticness preference: 0.48 (+0.05)
```

---

## Sample Recommendation Output

```text
============================================================
Top 5 Recommendations
============================================================

1. Sunrise City — Score: 0.98
   - Genre match: pop (+0.40)
   - Mood match: happy (+0.30)
   - Energy closeness: 0.82 vs target 0.80 (+0.20)
   - Low acousticness preference: 0.18 (+0.08)

2. Gym Hero — Score: 0.67
   - Genre match: pop (+0.40)
   - Mood mismatch: intense vs happy (0.00)
   - Energy closeness: 0.93 vs target 0.80 (+0.17)
   - Low acousticness preference: 0.05 (+0.10)

3. Rooftop Lights — Score: 0.56
   - Genre mismatch: indie pop vs pop (0.00)
   - Mood match: happy (+0.30)
   - Energy closeness: 0.76 vs target 0.80 (+0.19)
   - Low acousticness preference: 0.35 (+0.07)

4. Neon Dreams — Score: 0.27
   - Genre mismatch: electronic vs pop (0.00)
   - Mood mismatch: energetic vs happy (0.00)
   - Energy closeness: 0.88 vs target 0.80 (+0.18)
   - Low acousticness preference: 0.12 (+0.09)

5. Storm Runner — Score: 0.27
   - Genre mismatch: rock vs pop (0.00)
   - Mood mismatch: intense vs happy (0.00)
   - Energy closeness: 0.91 vs target 0.80 (+0.18)
   - Low acousticness preference: 0.10 (+0.09)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

**Weight Rebalancing: Doubling Energy, Halving Genre**

I tested swapping the importance of energy and genre to see if songs felt better when matching how a user wants to feel rather than what label the song has. I changed genre weight from 0.4 to 0.2 and energy weight from 0.2 to 0.4, then ran all 5 adversarial profiles to compare the before/after rankings. Profile 4 (classical + energetic) completely flipped—Neon Dreams (right mood/energy, wrong genre) jumped from 0.50 to 0.68 and now ranked #1, beating Moonlight Sonata which dropped from 0.58 to 0.47. This confirmed that genre-dominance was hiding poor energy fits, and that energy-first matching produces more intuitive results for conflicting or rare preference combinations.

---

**Expected Biases in This System:**

- **Genre/mood dominance**: Genre and mood are binary (exact match or nothing) and make up 70% of the score, while energy and acoustic use a more forgiving distance-based score. A musically-adjacent genre (e.g., "indie pop" vs. "pop") gets zero credit even if every numeric feature matches well, so the system can overprioritize categorical match over actual "feel" fit.
- **Catalog imbalance**: `lofi` and `pop` have multiple entries in the dataset while `classical`, `metal`, and `folk` have only one each. A user favoring an underrepresented genre will get fewer (or zero) genre matches, skewing results toward whatever is overrepresented in the catalog rather than reflecting genuine taste quality.
- **Weak acoustic signal**: `likes_acoustic` carries only 10% of the total score, so a stated acoustic preference can be nearly invisible in the final ranking when it conflicts with genre and mood preferences.

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)


**How Recommenders Turn Data Into Predictions:**
Recommenders are fundamentally just math as they assign numeric weights to different signals (in this system, 0.2 for genre, 0.3 for mood, 0.4 for energy, 0.1 for acousticness) and compute a score for every item, then rank by that score. When I doubled energy's weight from 0.2 to 0.4, profiles that ranked one way suddenly ranked completely differently, showing that recommendations are only as good as the priorities embedded in them. A recommender doesn't "learn" user preferences the way humans do instead it mechanically applies a formula. This means it will always be limited by what data it has (my system only sees genre, mood, energy, and acousticness therefore excluding artist, lyrics, cultural moment, or friend recommendations) and will always reflect the builder's assumptions about what matters.

**Where Bias and Unfairness Hide:**
Bias creeps in at every level. The dataset itself is biased as it's limited with only 18 songs. Pop and lofi are overrepresented while classical, metal, and folk each have just one entry, so users preferring underrepresented genres naturally get worse recommendations. The weights are also biased: by choosing 0.4 for energy, how intense a song is matters more than what genre it's labeled as which is a design choice and not a literal fact. The system also discriminates against users with extreme preferences (energy 0.0 or 1.0 scores poorly) and favors users with middle-ground tastes, because the distance-based scoring naturally clusters toward the center.


