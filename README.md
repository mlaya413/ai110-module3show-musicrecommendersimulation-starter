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

## Evaluation: Profile Results

`python -m src.main` runs seven profiles defined in `src/main.py`: three realistic ones (High-Energy Pop, Chill Lofi, Deep Intense Rock) and four adversarial edge cases meant to trick the scoring logic. Full terminal output (top 5 per profile):

```
Loaded songs: 18

================================================================
PROFILE: High-Energy Pop
genre=pop, mood=happy, energy=0.8, valence=0.8, likes_acoustic=False
Top 5 recommendations
================================================================

#1  Sunrise City by Neon Echo [pop/happy]
    Score: 9.85 / 10.00
    Reasons:
      - mood match: happy (+2.5)
      - genre match: pop (+1.5)
      - energy 0.82 vs target 0.80 (+3.43)
      - valence 0.84 vs target 0.80 (+1.44)
      - acousticness 0.18 vs target 0.20 (+0.98)

#2  Rooftop Lights by Indigo Parade [indie pop/happy]
    Score: 8.19 / 10.00
    Reasons:
      - mood match: happy (+2.5)
      - energy 0.76 vs target 0.80 (+3.36)
      - valence 0.81 vs target 0.80 (+1.48)
      - acousticness 0.35 vs target 0.20 (+0.85)

#3  Gym Hero by Max Pulse [pop/intense]
    Score: 6.85 / 10.00
    Reasons:
      - genre match: pop (+1.5)
      - energy 0.93 vs target 0.80 (+3.04)
      - valence 0.77 vs target 0.80 (+1.46)
      - acousticness 0.05 vs target 0.20 (+0.85)

#4  Concrete Crown by Kid Meridian [hip hop/confident]
    Score: 5.54 / 10.00
    Reasons:
      - energy 0.78 vs target 0.80 (+3.43)
      - valence 0.62 vs target 0.80 (+1.23)
      - acousticness 0.08 vs target 0.20 (+0.88)

#5  Night Drive Loop by Neon Echo [synthwave/moody]
    Score: 5.34 / 10.00
    Reasons:
      - energy 0.75 vs target 0.80 (+3.32)
      - valence 0.49 vs target 0.80 (+1.03)
      - acousticness 0.22 vs target 0.20 (+0.98)

================================================================
PROFILE: Chill Lofi
genre=lofi, mood=chill, energy=0.4, valence=0.6, likes_acoustic=True
Top 5 recommendations
================================================================

#1  Midnight Coding by LoRoom [lofi/chill]
    Score: 9.78 / 10.00
    Reasons:
      - mood match: chill (+2.5)
      - genre match: lofi (+1.5)
      - energy 0.42 vs target 0.40 (+3.43)
      - valence 0.56 vs target 0.60 (+1.44)
      - acousticness 0.71 vs target 0.80 (+0.91)

#2  Library Rain by Paper Lanterns [lofi/chill]
    Score: 9.76 / 10.00
    Reasons:
      - mood match: chill (+2.5)
      - genre match: lofi (+1.5)
      - energy 0.35 vs target 0.40 (+3.32)
      - valence 0.60 vs target 0.60 (+1.50)
      - acousticness 0.86 vs target 0.80 (+0.94)

#3  Spacewalk Thoughts by Orbit Bloom [ambient/chill]
    Score: 7.88 / 10.00
    Reasons:
      - mood match: chill (+2.5)
      - energy 0.28 vs target 0.40 (+3.08)
      - valence 0.65 vs target 0.60 (+1.42)
      - acousticness 0.92 vs target 0.80 (+0.88)

#4  Focus Flow by LoRoom [lofi/focused]
    Score: 7.46 / 10.00
    Reasons:
      - genre match: lofi (+1.5)
      - energy 0.40 vs target 0.40 (+3.50)
      - valence 0.59 vs target 0.60 (+1.48)
      - acousticness 0.78 vs target 0.80 (+0.98)

#5  Coffee Shop Stories by Slow Stereo [jazz/relaxed]
    Score: 5.64 / 10.00
    Reasons:
      - energy 0.37 vs target 0.40 (+3.40)
      - valence 0.71 vs target 0.60 (+1.33)
      - acousticness 0.89 vs target 0.80 (+0.91)

================================================================
PROFILE: Deep Intense Rock
genre=rock, mood=intense, energy=0.92, valence=0.45, likes_acoustic=False
Top 5 recommendations
================================================================

#1  Storm Runner by Voltline [rock/intense]
    Score: 9.82 / 10.00
    Reasons:
      - mood match: intense (+2.5)
      - genre match: rock (+1.5)
      - energy 0.91 vs target 0.92 (+3.46)
      - valence 0.48 vs target 0.45 (+1.46)
      - acousticness 0.10 vs target 0.20 (+0.90)

#2  Gym Hero by Max Pulse [pop/intense]
    Score: 7.83 / 10.00
    Reasons:
      - mood match: intense (+2.5)
      - energy 0.93 vs target 0.92 (+3.46)
      - valence 0.77 vs target 0.45 (+1.02)
      - acousticness 0.05 vs target 0.20 (+0.85)

#3  Night Drive Loop by Neon Echo [synthwave/moody]
    Score: 5.32 / 10.00
    Reasons:
      - energy 0.75 vs target 0.92 (+2.90)
      - valence 0.49 vs target 0.45 (+1.44)
      - acousticness 0.22 vs target 0.20 (+0.98)

#4  Iron Cathedral by Hollow Vanguard [metal/aggressive]
    Score: 5.31 / 10.00
    Reasons:
      - energy 0.97 vs target 0.92 (+3.33)
      - valence 0.22 vs target 0.45 (+1.16)
      - acousticness 0.03 vs target 0.20 (+0.83)

#5  Concrete Crown by Kid Meridian [hip hop/confident]
    Score: 5.13 / 10.00
    Reasons:
      - energy 0.78 vs target 0.92 (+3.01)
      - valence 0.62 vs target 0.45 (+1.25)
      - acousticness 0.08 vs target 0.20 (+0.88)

================================================================
PROFILE: ADVERSARIAL: Sad but Energetic
genre=folk, mood=melancholic, energy=0.9, valence=0.2, likes_acoustic=False
Top 5 recommendations
================================================================

#1  Autumn Letters by Fern & Ash [folk/melancholic]
    Score: 7.11 / 10.00
    Reasons:
      - mood match: melancholic (+2.5)
      - genre match: folk (+1.5)
      - energy 0.30 vs target 0.90 (+1.40)
      - valence 0.25 vs target 0.20 (+1.42)
      - acousticness 0.91 vs target 0.20 (+0.29)

#2  Iron Cathedral by Hollow Vanguard [metal/aggressive]
    Score: 5.56 / 10.00
    Reasons:
      - energy 0.97 vs target 0.90 (+3.26)
      - valence 0.22 vs target 0.20 (+1.47)
      - acousticness 0.03 vs target 0.20 (+0.83)

#3  Storm Runner by Voltline [rock/intense]
    Score: 5.45 / 10.00
    Reasons:
      - energy 0.91 vs target 0.90 (+3.46)
      - valence 0.48 vs target 0.20 (+1.08)
      - acousticness 0.10 vs target 0.20 (+0.90)

#4  Night Drive Loop by Neon Echo [synthwave/moody]
    Score: 5.02 / 10.00
    Reasons:
      - energy 0.75 vs target 0.90 (+2.98)
      - valence 0.49 vs target 0.20 (+1.06)
      - acousticness 0.22 vs target 0.20 (+0.98)

#5  Gym Hero by Max Pulse [pop/intense]
    Score: 4.89 / 10.00
    Reasons:
      - energy 0.93 vs target 0.90 (+3.40)
      - valence 0.77 vs target 0.20 (+0.64)
      - acousticness 0.05 vs target 0.20 (+0.85)

================================================================
PROFILE: ADVERSARIAL: Acoustic Metalhead
genre=metal, mood=aggressive, energy=0.97, valence=0.22, likes_acoustic=True
Top 5 recommendations
================================================================

#1  Iron Cathedral by Hollow Vanguard [metal/aggressive]
    Score: 9.23 / 10.00
    Reasons:
      - mood match: aggressive (+2.5)
      - genre match: metal (+1.5)
      - energy 0.97 vs target 0.97 (+3.50)
      - valence 0.22 vs target 0.22 (+1.50)
      - acousticness 0.03 vs target 0.80 (+0.23)

#2  Storm Runner by Voltline [rock/intense]
    Score: 4.70 / 10.00
    Reasons:
      - energy 0.91 vs target 0.97 (+3.29)
      - valence 0.48 vs target 0.22 (+1.11)
      - acousticness 0.10 vs target 0.80 (+0.30)

#3  Gym Hero by Max Pulse [pop/intense]
    Score: 4.29 / 10.00
    Reasons:
      - energy 0.93 vs target 0.97 (+3.36)
      - valence 0.77 vs target 0.22 (+0.67)
      - acousticness 0.05 vs target 0.80 (+0.25)

#4  Night Drive Loop by Neon Echo [synthwave/moody]
    Score: 4.25 / 10.00
    Reasons:
      - energy 0.75 vs target 0.97 (+2.73)
      - valence 0.49 vs target 0.22 (+1.09)
      - acousticness 0.22 vs target 0.80 (+0.42)

#5  Pulse Horizon by Kairo Wave [edm/euphoric]
    Score: 4.15 / 10.00
    Reasons:
      - energy 0.95 vs target 0.97 (+3.43)
      - valence 0.90 vs target 0.22 (+0.48)
      - acousticness 0.04 vs target 0.80 (+0.24)

================================================================
PROFILE: ADVERSARIAL: Unknown Genre and Mood
genre=bossa nova, mood=dreamy, energy=0.5, valence=0.7, likes_acoustic=True
Top 5 recommendations
================================================================

#1  Dusty Porchlight by Wren Hollow [country/nostalgic]
    Score: 5.84 / 10.00
    Reasons:
      - energy 0.52 vs target 0.50 (+3.43)
      - valence 0.68 vs target 0.70 (+1.47)
      - acousticness 0.74 vs target 0.80 (+0.94)

#2  Focus Flow by LoRoom [lofi/focused]
    Score: 5.46 / 10.00
    Reasons:
      - energy 0.40 vs target 0.50 (+3.15)
      - valence 0.59 vs target 0.70 (+1.33)
      - acousticness 0.78 vs target 0.80 (+0.98)

#3  Coffee Shop Stories by Slow Stereo [jazz/relaxed]
    Score: 5.44 / 10.00
    Reasons:
      - energy 0.37 vs target 0.50 (+3.04)
      - valence 0.71 vs target 0.70 (+1.48)
      - acousticness 0.89 vs target 0.80 (+0.91)

#4  Midnight Coding by LoRoom [lofi/chill]
    Score: 5.42 / 10.00
    Reasons:
      - energy 0.42 vs target 0.50 (+3.22)
      - valence 0.56 vs target 0.70 (+1.29)
      - acousticness 0.71 vs target 0.80 (+0.91)

#5  Velvet Hours by Satin Avenue [r&b/romantic]
    Score: 5.33 / 10.00
    Reasons:
      - energy 0.55 vs target 0.50 (+3.32)
      - valence 0.72 vs target 0.70 (+1.47)
      - acousticness 0.34 vs target 0.80 (+0.54)

================================================================
PROFILE: ADVERSARIAL: Dead Center
genre=pop, mood=happy, energy=0.5, valence=0.5, likes_acoustic=False
Top 5 recommendations
================================================================

#1  Sunrise City by Neon Echo [pop/happy]
    Score: 8.35 / 10.00
    Reasons:
      - mood match: happy (+2.5)
      - genre match: pop (+1.5)
      - energy 0.82 vs target 0.50 (+2.38)
      - valence 0.84 vs target 0.50 (+0.99)
      - acousticness 0.18 vs target 0.20 (+0.98)

#2  Rooftop Lights by Indigo Parade [indie pop/happy]
    Score: 6.97 / 10.00
    Reasons:
      - mood match: happy (+2.5)
      - energy 0.76 vs target 0.50 (+2.59)
      - valence 0.81 vs target 0.50 (+1.03)
      - acousticness 0.35 vs target 0.20 (+0.85)

#3  Gym Hero by Max Pulse [pop/intense]
    Score: 5.44 / 10.00
    Reasons:
      - genre match: pop (+1.5)
      - energy 0.93 vs target 0.50 (+1.99)
      - valence 0.77 vs target 0.50 (+1.09)
      - acousticness 0.05 vs target 0.20 (+0.85)

#4  Velvet Hours by Satin Avenue [r&b/romantic]
    Score: 5.35 / 10.00
    Reasons:
      - energy 0.55 vs target 0.50 (+3.32)
      - valence 0.72 vs target 0.50 (+1.17)
      - acousticness 0.34 vs target 0.20 (+0.86)

#5  Dusty Porchlight by Wren Hollow [country/nostalgic]
    Score: 5.12 / 10.00
    Reasons:
      - energy 0.52 vs target 0.50 (+3.43)
      - valence 0.68 vs target 0.50 (+1.23)
      - acousticness 0.74 vs target 0.20 (+0.46)
```

### What the adversarial profiles showed

- **Sad but Energetic** (folk, melancholic, energy 0.9, valence 0.2): this conflict has no good answer in the catalog, and the system reflects that. The only song matching the mood and genre, Autumn Letters (energy 0.30), still wins at 7.11 because the 4.0 points from its two label matches outweigh losing about 2.1 energy points. The next songs (Iron Cathedral, Storm Runner) are the loud, dark ones, which is a sensible compromise. The top result, though, has the opposite energy of what the user asked for.
- **Acoustic Metalhead** (metal, aggressive, energy 0.97, likes_acoustic): Iron Cathedral wins easily (9.23) even though its acousticness is 0.03 against a target of 0.8. Acousticness is worth only 1.0 point, so a preference that contradicts the user's other tastes is nearly ignored. After #1 the scores fall to about 4 to 4.7, so the list becomes a generic "loud and dark" set with the acoustic preference having no visible effect.
- **Unknown Genre and Mood** (bossa nova, dreamy): no song can earn any label points, so the ranking falls back to numeric closeness only, and the max possible score drops to 6.0. The results are reasonable (acoustic, mid-energy songs), but all five scores sit between 5.3 and 5.9, so the ordering is nearly arbitrary. The system cannot tell the user that it found no genre or mood match.
- **Dead Center** (pop, happy, energy 0.5, valence 0.5): Sunrise City still wins (8.35) despite its energy being 0.32 away from the target. The label matches (4.0 points) outweigh the energy gap, so "middle of the road" users are pulled toward songs that match their labels, not their numbers. Gym Hero (energy 0.93) lands in the top 3 on its genre match alone.

### Other observations

- Across the realistic profiles, the top result is a near-perfect match (9.78 to 9.85), and the system separates "Chill Lofi" from "Deep Intense Rock" cleanly: no song appears in both top 5 lists.
- Gym Hero keeps showing up for pop and rock users. It earns points for the genre or mood match plus very high energy, which gives it the highest score among non-matching songs for several profiles.
- The 2.5 mood weight and 1.5 genre weight can overrule the numeric features, which is a deliberate choice but is exactly where the conflicting profiles "trick" the system.

---

## Experiments You Tried

### Experiment 1: Weight shift (energy x2, genre x0.5)

**Change:** energy 3.5 -> 7.0 points and genre 1.5 -> 0.75 points. The maximum score rises from 10.0 to 12.75 (7.0 + 2.5 + 1.5 + 0.75 + 1.0), so scores are no longer out of 10. I added a `MAX_SCORE` constant, computed from the weights, so the printed denominator stays correct. Ranking is unaffected by the larger maximum because every song is scored on the same scale. I reverted the weights afterward, so the sample output above reflects the original recipe.

**Result: different, and only sometimes more accurate.** The top 2 songs were identical for all three realistic profiles, and the pop and lofi top 5 lists did not change at all. The changes showed up in the rock and adversarial profiles.

| Profile | Baseline | After weight shift | Better? |
|---|---|---|---|
| Deep Intense Rock | #3 Night Drive Loop, #4 Iron Cathedral, #5 Concrete Crown | Iron Cathedral rises to #3, but Pulse Horizon (EDM, euphoric, valence 0.90) enters at #4 | Mixed: metal is closer to the intent, but a happy EDM track now sneaks in on energy alone |
| Sad but Energetic | #1 Autumn Letters (sad but quiet) | #1 Storm Runner (loud, valence 0.48) | Arguably yes: it no longer recommends a quiet song to a user who asked for energy 0.9 |
| Dead Center (pop/happy, energy 0.5) | Gym Hero (energy 0.93) at #3 | Gym Hero dropped out; Velvet Hours and Dusty Porchlight (energy about 0.5) moved up | Yes: results now match the energy the user asked for |
| Unknown Genre and Mood | Dusty Porchlight, Focus Flow, Coffee Shop Stories... | Same top song, middle of the list reshuffled | Different only; the scores are still nearly tied |

**Takeaway:** doubling energy makes the system follow the numbers more closely, which helps when the labels conflict with the targets. It also lets high-energy songs with the wrong feel (Pulse Horizon for a rock fan) rise, because energy alone cannot tell an aggressive song from a euphoric one. Because I changed both weights at once, I can't say how much of the shift came from genre alone. The better fix for the "intense vs aggressive" mismatch is still partial credit for similar moods, not re-weighting.

### Ideas still to test

- Partial credit for near-synonym moods (intense ~ aggressive, chill ~ relaxed ~ peaceful)
- Removing the mood check entirely
- Adding tempo or danceability to the score

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



