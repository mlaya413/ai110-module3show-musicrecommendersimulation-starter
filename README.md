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

### Real-world recommenders vs. this version

Real platforms like Spotify and YouTube combine two ideas. *Collaborative filtering* learns from the behavior of millions of users (plays, skips, saves, playlist adds, watch time) to find songs that similar listeners enjoyed. *Content-based filtering* compares the attributes of a song (tempo, energy, mood, audio analysis) to what a user already likes, which also works for brand-new songs with no listening history. My simulation has no other users, so it is purely **content-based**. It prioritizes the *vibe* of a song: how close its energy and emotional tone (valence) are to what the user wants, followed by a mood match, with genre and acousticness as smaller nudges. It rewards songs for being *close* to the user's preference, not for being high or low on a feature.

### Features used

**`Song`** (from `data/songs.csv`): `id`, `title`, `artist`, `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness`. The scoring rule uses `energy`, `valence`, `mood`, `genre`, and `acousticness`. Tempo and danceability are loaded but unused at first because they largely track energy.

**`UserProfile`**: `favorite_genre`, `favorite_mood`, `target_energy` (0–1), `likes_acoustic` (bool), plus a planned optional `target_valence` (0–1).

### Algorithm Recipe (Scoring Rule for one song)

Each song earns points out of a maximum of **10.0**:

| Rule | Points | How it is computed |
|---|---|---|
| Energy closeness | up to **+3.5** | `3.5 * (1 - abs(song.energy - target_energy))` |
| Mood match | **+2.5** | `+2.5` if `song.mood == favorite_mood`, else 0 |
| Valence closeness | up to **+1.5** | `1.5 * (1 - abs(song.valence - target_valence))` |
| Genre match | **+1.5** | `+1.5` if `song.genre == favorite_genre`, else 0 |
| Acousticness closeness | up to **+1.0** | `1.0 * (1 - abs(song.acousticness - t))`, where `t = 0.8` if `likes_acoustic` else `0.2` |

- **Numeric features reward closeness, not size.** A user targeting energy 0.40 gets 3.43 points from a song at 0.35 and 1.65 from a song at 0.93. Overshooting is penalized just like undershooting.
- **Categorical features are all-or-nothing.**
- **Why mood (2.5) outweighs genre (1.5):** the common starting point is genre +2.0 and mood +1.0, but I'm deliberately flipping it. Genre is a coarse label that hides huge variety, and with 18 songs across 15 genres a genre match is rare, so a high genre weight would act as a hard filter and trap the user in one bucket. Mood is closer to what a "vibe" is and crosses genres (a chill lofi track and a relaxed jazz track can satisfy the same listener). Energy gets the most points because it was the strongest separator in the data. The genre-vs-mood weights are the first thing I'll vary in the Experiments section.
- **Left out for now:** `tempo_bpm` and `danceability` largely track energy, so including them would double-count it.

### Taste profile used for testing

```python
user_profile = {
    "favorite_genre": "lofi",
    "favorite_mood": "chill",
    "target_energy": 0.40,
    "target_valence": 0.60,
    "likes_acoustic": True,
}
```

A hand check with this profile gives Midnight Coding (lofi, chill) about 9.8, Coffee Shop Stories (jazz, relaxed) about 5.6, and Storm Runner (rock, intense) about 3.3, so the profile cleanly separates "chill lofi" from "intense rock."

### Ranking Rule (list of songs)

Apply the Scoring Rule to every song in the catalog, sort by score in descending order, and return the top `k`. Ties are broken by title for stable output. Each result also carries a short explanation built from the features that contributed most to its score.

**Why both rules are needed:** the Scoring Rule judges one song in isolation and answers "how well does this song fit this user?" It cannot decide what to *show*. The Ranking Rule works across the whole list: it compares scores, orders them, and cuts the list to `k`. Without scoring there is nothing to compare, and without ranking you have a pile of numbers rather than a recommendation. Separating them also lets me change one without touching the other, for example adding a diversity filter to the ranking step without altering how songs are scored.

### Expected biases

- **Energy dominance:** energy is worth the most points (3.5 of 10), so a song with the right energy but the wrong mood and genre can still outrank a song that matches the user's mood. Energy closeness alone cannot tell a joyful high-energy song from an aggressive one, which is why valence is included.
- **Exact-match categories:** mood and genre are all-or-nothing, so "peaceful" earns nothing for a user who wants "chill" even though they are nearly the same vibe. Near-misses are punished as hard as total misses.
- **Single-taste profile:** one target per feature cannot represent a user who likes both gym and study music.
- **Tiny, uneven catalog:** lofi has 3 songs and most genres have 1, so users who prefer lofi get more good options than users who prefer, say, metal. The dataset and my own weight choices also encode my assumptions about what a "vibe" is.
- **Genre under-weighting:** the reverse risk of my choice. A listener who really cares about genre may see off-genre songs ranked above it.

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

Output of `python -m src.main` for the default pop/happy profile (`target_valence=0.80`, `likes_acoustic=False`) on the 18-song catalog:

```
Loaded songs: 18

================================================================
User profile: genre=pop, mood=happy, energy=0.8
Top 5 recommendations
================================================================

#1  Sunrise City by Neon Echo
    Score: 9.85 / 10.00
    Reasons:
      - mood match: happy (+2.5)
      - genre match: pop (+1.5)
      - energy 0.82 vs target 0.80 (+3.43)
      - valence 0.84 vs target 0.80 (+1.44)
      - acousticness 0.18 vs target 0.20 (+0.98)

#2  Rooftop Lights by Indigo Parade
    Score: 8.19 / 10.00
    Reasons:
      - mood match: happy (+2.5)
      - energy 0.76 vs target 0.80 (+3.36)
      - valence 0.81 vs target 0.80 (+1.48)
      - acousticness 0.35 vs target 0.20 (+0.85)

#3  Gym Hero by Max Pulse
    Score: 6.85 / 10.00
    Reasons:
      - genre match: pop (+1.5)
      - energy 0.93 vs target 0.80 (+3.04)
      - valence 0.77 vs target 0.80 (+1.46)
      - acousticness 0.05 vs target 0.20 (+0.85)

#4  Concrete Crown by Kid Meridian
    Score: 5.54 / 10.00
    Reasons:
      - energy 0.78 vs target 0.80 (+3.43)
      - valence 0.62 vs target 0.80 (+1.23)
      - acousticness 0.08 vs target 0.20 (+0.88)

#5  Night Drive Loop by Neon Echo
    Score: 5.34 / 10.00
    Reasons:
      - energy 0.75 vs target 0.80 (+3.32)
      - valence 0.49 vs target 0.80 (+1.03)
      - acousticness 0.22 vs target 0.20 (+0.98)

================================================================
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

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



