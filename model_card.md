# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

This recommender works like a friend who knows your taste and checks each song in a list against it, one at a time. It is "content-based": it only looks at what a song is like, not at what other listeners did. Real apps like Spotify also learn from millions of listeners' plays and skips. Mine has no other users, so it can't do that.

**What it knows about you.** Your favorite genre, your favorite mood, how energetic you want the music, how happy or dark you want it to sound, and whether you like acoustic (unplugged, organic) music.

**What it knows about each song.** Its genre, mood, energy, valence (how happy it sounds), and acousticness.

**How a song gets its score.** Every song starts at zero and earns up to 10 points:
- **Energy (up to 3.5 points).** The closer the song's energy is to what you want, the more points. A calm song is not "worse" than a loud one. It only loses points when it is far from your target, whether too loud or too quiet.
- **Mood (2.5 points).** All or nothing: you get them if the song's mood is the one you asked for.
- **Valence (up to 1.5 points).** Same idea as energy, for how happy or dark the song sounds. This is what separates an upbeat workout song from an angry one.
- **Genre (1.5 points).** All or nothing, like mood.
- **Acousticness (up to 1 point).** The closer to your acoustic preference, the more points.

I put mood above genre on purpose. Genre is a broad label, and a chill jazz song and a chill lofi song can feel the same, while two songs in the same genre can feel completely different.

**How it picks songs.** It scores every song in the catalog, sorts them from highest to lowest, and shows the top five. For each one it also lists the exact points it earned, so you can see why it was recommended.

**Changes from the starter.** The starter returned the first songs in the file with no scoring. I added the CSV loader, the point system, the ranking, and the explanations, plus a `target_valence` setting for the user.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
