# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world recommenders like Spotify or YouTube blend two main strategies: collaborative filtering, which predicts what a listener will like based on the behavior of other users with similar taste, and content-based filtering, which matches a song's own attributes (genre, tempo, mood) against a listener's known preferences. Production systems combine both, plus signals like NLP-mined cultural context, so they can recommend brand-new songs with no listening history yet as well as songs backed by strong social proof. Our simulation implements only the content-based half: each `Song` carries genre, mood, energy, tempo_bpm, valence, danceability, and acousticness, and each `UserProfile` stores a single listener's favorite_genre, favorite_mood, target_energy, and likes_acoustic preference. The `Recommender` scores every song by combining a categorical match on genre and mood (weighted most heavily, since they capture most of what makes a song feel "right") with a numeric closeness score on energy, computed as `1 - |song_energy - target_energy|` so songs are rewarded for being close to the user's target rather than simply high or low energy. Songs are then ranked by total score and the top `k` are returned as recommendations. Because there's no data on other listeners, our system can't yet capture "people like you also liked" style discovery unlike real platforms that use collaborative filtering to introduce discovery. This recommender will always lean toward recommending more of what a user already says they like.

**Scoring Formula:**

```
total_score = (0.4 × genre_match) + (0.3 × mood_match) + (0.2 × energy_score) + (0.1 × acoustic_score)

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

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

**Expected Biases in This System:**

- **Genre/mood dominance**: Genre and mood are binary (exact match or nothing) and make up 70% of the score, while energy and acoustic use a more forgiving distance-based score. A musically-adjacent genre (e.g., "indie pop" vs. "pop") gets zero credit even if every numeric feature matches well, so the system can overprioritize categorical match over actual "feel" fit.
- **Catalog imbalance**: `lofi` and `pop` have multiple entries in the dataset while `classical`, `metal`, and `folk` have only one each. A user favoring an underrepresented genre will get fewer (or zero) genre matches, skewing results toward whatever is overrepresented in the catalog rather than reflecting genuine taste quality.
- **Weak acoustic signal**: `likes_acoustic` carries only 10% of the total score, so a stated acoustic preference can be nearly invisible in the final ranking when it conflicts with genre and mood preferences.

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



