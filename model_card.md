# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeFinder 1.0**

A small, point-based music recommender that runs in the terminal.

---

## 2. Intended Use  

**Goal / Task.** VibeFinder suggests the top 5 songs from a small catalog for one listener. It tries to predict which songs match the vibe the user asked for. Vibe means genre, mood, energy, happiness, and how acoustic the song is.

**What it assumes about the user.**
- The user can describe their taste with one genre, one mood, and one energy level.
- The user wants one kind of music at a time.

**Intended use.** This is a classroom project. It is for learning how recommenders turn data into a ranked list. Every result comes with a list of reasons, so it is easy to inspect.

**Not intended for.**
- Real users or a real music app. The catalog is tiny and made up.
- Guessing anything about a person, like their mood or mental state.
- Deciding which artists get exposure or money.
- People with mixed tastes, or tastes that depend on lyrics, language, or culture. It does not understand those.

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

- **Size:** 18 songs in `data/songs.csv`. The starter had 10. I added 8.
- **Columns:** id, title, artist, genre, mood, energy, tempo_bpm, valence, danceability, acousticness.
- **Variety:** 15 genres and 14 moods. Most genres have only one song. Lofi has three.
- **Used in scoring:** genre, mood, energy, valence, and acousticness.
- **Loaded but not used:** tempo_bpm and danceability. They mostly move with energy.
- **Limits:**
  - The songs and artists are made up. The numbers are my best guesses, not real measurements.
  - 18 songs is very small, so there is little to choose from.
  - There are no lyrics, no language, no release year, and no popularity data.
  - There is no data about other listeners.
  - Many kinds of taste are missing, like world music, gospel, or country sub-styles.

---

## 5. Strengths  

- **Everyday profiles work well.** Happy Pop, Chill Lofi, and Deep Intense Rock each put an obvious song first, with scores near 9.8 out of 10.
- **It tells different vibes apart.** The Chill Lofi and Deep Intense Rock lists share no songs.
- **Mood can cross genres.** A chill ambient song ranked high for a lofi fan, which is what I hoped for.
- **Closeness works.** A song is not rewarded just for being loud or quiet. It earns points for being near what the user wants.
- **It explains itself.** Every song comes with a plain list of the points it earned, so it is easy to see why it ranked where it did.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

**Weakness found in testing: exact-match labels can outweigh how a song actually sounds.** Mood and genre are all-or-nothing, so "aggressive" earns no credit for a user who asked for "intense," even though the two mean nearly the same thing. In the Deep Intense Rock test, Gym Hero (a happy pop workout track, valence 0.77) ranked #2 because its mood label was "intense," while Iron Cathedral (dark metal, valence 0.22, much closer to the requested sound) fell to #4 with no mood match. The catalog makes this worse: only 18 songs spread over 15 genres means most genres have a single song, and "indie pop" does not count as "pop," so Rooftop Lights misses the genre bonus for a pop fan. Users whose tastes happen to match the larger groups, like lofi with 3 songs, get more songs earning both label bonuses than users who like metal, country or classical.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

### Profiles tested

I ran seven profiles against the 18-song catalog and looked at the top 5 for each. Full output is in the README.

- **Three everyday listeners:** High-Energy Pop (pop, happy, energy 0.8), Chill Lofi (lofi, chill, energy 0.4, likes acoustic), and Deep Intense Rock (rock, intense, energy 0.92).
- **Four "trick" profiles:** Sad but Energetic (wants a melancholic folk mood but energy 0.9), Acoustic Metalhead (metal that is also acoustic), Unknown Genre and Mood (asks for "bossa nova" and "dreamy," which no song has), and Dead Center (pop/happy but with every number set to the middle).

What I checked: whether the #1 song made sense, whether the top 5 as a whole fit the described vibe, and whether the score breakdown ("reasons") explained the result.

### Comparing the profiles

I compared the profiles in pairs. These are the ones that taught me the most.

- **Pop vs. Lofi:** no songs in common. Pop gets bright, loud tracks (Sunrise City, Rooftop Lights, Gym Hero), while Lofi gets quiet, soft ones (Midnight Coding, Library Rain, Spacewalk Thoughts). That is what I wanted: the energy target and the mood label pull in opposite directions, and the lists move accordingly.
- **Lofi vs. Rock:** also nothing in common. Rock's list is all loud and dark (Storm Runner, Iron Cathedral). Lofi's is all quiet and soft. This is the clearest proof that the system can tell "chill lofi" from "intense rock."
- **Pop vs. Rock:** three of five songs overlap (Gym Hero, Night Drive Loop, Concrete Crown). Both users want loud music, so the energy score pulls the same songs up for both. What differs is the top: Pop gets the cheerful Sunrise City, Rock gets the harder Storm Runner. The shared songs show energy is doing most of the work.
- **Rock vs. Acoustic Metalhead:** both want very loud, dark music, so both lists are Storm Runner, Gym Hero and Night Drive Loop, with Iron Cathedral at #1 for the metalhead. The "likes acoustic" setting changed almost nothing. A real acoustic fan would hate this list, so the system is not honoring that preference.
- **Rock vs. Sad but Energetic:** both want loud, dark songs, so Iron Cathedral and Storm Runner appear in both. The difference is #1: the sad profile gets Autumn Letters, a quiet folk song. The sad mood and folk genre labels were worth more points than the loud-music request, so the system gave this user a song that is the opposite of "energetic."
- **Lofi vs. Unknown Genre and Mood:** the unknown profile wanted mid energy and acoustic sound, and got a mix of lofi, jazz, country and R&B. That is sensible: with no label matches, the system fell back to the numbers. But the five scores are almost tied (5.3 to 5.8), so the order is close to arbitrary, and the system never says "I found nothing that matches your genre or mood."
- **Pop vs. Dead Center:** same labels, different numbers. Moving the targets to the middle swapped the last two songs, Concrete Crown and Night Drive Loop, for mid-energy ones (Velvet Hours and Dusty Porchlight). The top three stayed the same, including the loud workout track Gym Hero. Sunrise City still came first even though it is loud, because both label matches (4 points) outweigh being off on energy. So the labels are probably too strong.
- **Sad but Energetic vs. Acoustic Metalhead:** both have a conflict in them. When labels and numbers disagree (sad vs. energetic), the labels won. When two numbers disagree (loud vs. acoustic), the bigger number won. In both cases the smaller preference got ignored.

### What surprised me

1. **Gym Hero shows up in five of seven lists.** See the plain-language explanation below.
2. **A quiet song topped the "energetic" profile**, because labels beat numbers.
3. **The acoustic setting hardly mattered.** It is worth only 1 point out of 10, so any other preference overrides it.
4. **A user whose tastes are not in the catalog still gets a confident-looking answer.** The system always produces five songs and never says "no good match."

### Why does "Gym Hero" keep showing up for people who just want Happy Pop?

Think of the system as a judge handing out points. Gym Hero is a pop song, so it gets the genre points. It is loud and upbeat, which is close to what a Happy Pop fan wants, so it gets most of the energy and happiness points too. The only thing it lacks is the "happy" label, because it is tagged "intense." That one miss costs it 2.5 points. But the catalog only has 18 songs and only two pop songs. Once Sunrise City and Rooftop Lights (the only "happy" songs) have been picked, Gym Hero is the best remaining song for a pop fan. It is not that the system thinks Gym Hero is happy. There are simply not many other songs to choose from. It also reaches the lists for rock and metal fans, since it is loud and has the "intense" label. A bigger catalog would fix most of this.

### Logic experiment: doubling energy and halving genre

I doubled the points for energy (3.5 to 7.0) and halved the points for genre (1.5 to 0.75). The top songs barely moved for the everyday profiles, but two of the trick profiles improved: Dead Center dropped Gym Hero for songs that really are mid-energy, and Sad but Energetic now puts a loud song first. However, Deep Intense Rock started recommending a happy EDM track because it is loud. So the change made the system follow energy more strictly, which fixed some mistakes and created others. I changed the weights back afterward. Details are in the README.

### Is it valid?

For ordinary profiles, yes: the top songs match what a person would expect, and the "reasons" make each choice easy to check. For profiles with conflicting preferences or tastes outside the catalog, no: it gives a confident answer that does not fit what the user asked for.

---

## 8. Future Work  

1. **Give partial credit for similar moods and genres.** "Aggressive" should earn some points for a user who asked for "intense," and "indie pop" should count a little as "pop."
2. **Add more songs, and warn when nothing matches.** A bigger catalog would fix most of the Gym Hero problem. If no song matches the user's genre or mood, the system should say so.
3. **Support more than one taste and add variety.** Let a user have two profiles, like "gym" and "study." Also make sure the top 5 are not all nearly the same song.

---

## 9. Personal Reflection  

I learned that a recommender can feel smart while being just a few point rules. The weights I picked decided almost everything. Changing two of them reshuffled whole lists.

The most surprising thing was Gym Hero. It kept showing up for people who never asked for it. It was not a bug. The catalog was just too small, and the label points were too strong.

This changed how I think about music apps. When Spotify gets it right, it is using far more than song attributes. It also uses the behavior of millions of listeners. When it gets it wrong, I will now wonder which small rule or missing data caused it.
