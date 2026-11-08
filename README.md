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

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

In every day life, your friends might suggest songs to you based on similar songs you already like, based on genre, artist, mood of the song and more. This version will try to match based on genre, mood, energy and acousticness. Song contains those features as well as store the songs title and artist. The UserProfile holds the preferences for the user, their preferred genres, mood, target energy and what acoustics they like. This allows the Recommender class to do the work and score each song for each UserProfile based on these, giving weight to whether it matches the profile's features. It then sorts the songs by which fit the best and recommends those.

The weights given right now are 1.5 to genre and energy, 1 to mood, 1 to valence/feeling, and 0.5 to other values such as instrumentalness that are recorded. This is to prevent one similarity from being too strong, however because energy, mood and valence have a slight overlapping it might weigh some songs too high because of this. 

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

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
Loading songs from data/songs.csv...
Loaded songs: 20

Top recommendations:

Sunrise City - Score: 4.95
Because: genre match (pop) (+1.50); mood match (happy) (+1.00); energy 0.82 vs target 0.85 (+1.47); valence 0.84 vs target 0.80 (+0.98)

Rooftop Lights - Score: 4.00
Because: partial genre match (indie pop) (+0.75); mood match (happy) (+1.00); energy 0.76 vs target 0.85 (+1.25); valence 0.81 vs target 0.80 (+1.00)

Gym Hero - Score: 3.79
Because: genre match (pop) (+1.50); energy 0.93 vs target 0.85 (+1.30); valence 0.77 vs target 0.80 (+0.99)

Storm Runner - Score: 3.16
Because: genre match (rock) (+1.50); energy 0.91 vs target 0.85 (+1.38); valence 0.48 vs target 0.80 (+0.28)

Banjo Breakdown - Score: 2.46
Because: energy 0.88 vs target 0.85 (+1.47); valence 0.83 vs target 0.80 (+0.99)
```
trying to use edge case profiles:
```
Loading songs from data/songs.csv...
Loaded songs: 20

Top recommendations:

Sunrise City - Score: 4.95
Because: genre match (pop) (+1.50); mood match (happy) (+1.00); energy 0.82 vs target 0.85 (+1.47); valence 0.84 vs target 0.80 (+0.98)

Rooftop Lights - Score: 4.00
Because: partial genre match (indie pop) (+0.75); mood match (happy) (+1.00); energy 0.76 vs target 0.85 (+1.25); valence 0.81 vs target 0.80 (+1.00)

Gym Hero - Score: 3.79
Because: genre match (pop) (+1.50); energy 0.93 vs target 0.85 (+1.30); valence 0.77 vs target 0.80 (+0.99)

Storm Runner - Score: 3.16
Because: genre match (rock) (+1.50); energy 0.91 vs target 0.85 (+1.38); valence 0.48 vs target 0.80 (+0.28)

Banjo Breakdown - Score: 2.46
Because: energy 0.88 vs target 0.85 (+1.47); valence 0.83 vs target 0.80 (+0.99)

linda@Mac ai110-module3show-musicrecommendersimulation-starter % git push origin main
Everything up-to-date
linda@Mac ai110-module3show-musicrecommendersimulation-starter % python3 -m src.main 
Loading songs from data/songs.csv...
Loaded songs: 20

=== Upbeat Pop/Rock ===
Preferences: {'genres': ['pop', 'rock'], 'mood': 'happy', 'energy': 0.85, 'valence': 0.8}

Sunrise City (pop, happy) - Score: 4.95
Because: genre match (pop) (+1.50); mood match (happy) (+1.00); energy 0.82 vs target 0.85 (+1.47); valence 0.84 vs target 0.80 (+0.98)

Rooftop Lights (indie pop, happy) - Score: 4.00
Because: partial genre match (indie pop) (+0.75); mood match (happy) (+1.00); energy 0.76 vs target 0.85 (+1.25); valence 0.81 vs target 0.80 (+1.00)

Gym Hero (pop, intense) - Score: 3.79
Because: genre match (pop) (+1.50); energy 0.93 vs target 0.85 (+1.30); valence 0.77 vs target 0.80 (+0.99)

Storm Runner (rock, intense) - Score: 3.16
Because: genre match (rock) (+1.50); energy 0.91 vs target 0.85 (+1.38); valence 0.48 vs target 0.80 (+0.28)

Banjo Breakdown (bluegrass, energetic) - Score: 2.46
Because: energy 0.88 vs target 0.85 (+1.47); valence 0.83 vs target 0.80 (+0.99)


=== Sad but Energetic ===
Preferences: {'mood': 'sad', 'energy': 0.9, 'valence': 0.2}

Iron Tide (metal, angry) - Score: 2.34
Because: energy 0.97 vs target 0.90 (+1.35); valence 0.19 vs target 0.20 (+1.00)

Empty Station (trip hop, sad) - Score: 2.00
Because: mood match (sad) (+1.00); valence 0.18 vs target 0.20 (+1.00)

Storm Runner (rock, intense) - Score: 1.87
Because: energy 0.91 vs target 0.90 (+1.50); valence 0.48 vs target 0.20 (+0.38)

Banjo Breakdown (bluegrass, energetic) - Score: 1.49
Because: energy 0.88 vs target 0.90 (+1.49); valence 0.83 vs target 0.20 (+0.01)

Gym Hero (pop, intense) - Score: 1.49
Because: energy 0.93 vs target 0.90 (+1.47); valence 0.77 vs target 0.20 (+0.02)


=== Acoustic EDM Fan ===
Preferences: {'genres': ['edm'], 'mood': 'euphoric', 'energy': 0.95, 'likes_acoustic': True}

Strobe Heart (edm, euphoric) - Score: 4.01
Because: genre match (edm) (+1.50); mood match (euphoric) (+1.00); energy 0.96 vs target 0.95 (+1.50); acousticness 0.02 fits acoustic preference (+0.01)

Banjo Breakdown (bluegrass, energetic) - Score: 1.82
Because: energy 0.88 vs target 0.95 (+1.35); acousticness 0.94 fits acoustic preference (+0.47)

Gym Hero (pop, intense) - Score: 1.51
Because: energy 0.93 vs target 0.95 (+1.49); acousticness 0.05 fits acoustic preference (+0.03)

Iron Tide (metal, angry) - Score: 1.50
Because: energy 0.97 vs target 0.95 (+1.49); acousticness 0.03 fits acoustic preference (+0.01)

Storm Runner (rock, intense) - Score: 1.50
Because: energy 0.91 vs target 0.95 (+1.45); acousticness 0.10 fits acoustic preference (+0.05)


=== Capitalized Input ===
Preferences: {'genres': ['Pop', 'Rock'], 'mood': 'Happy', 'energy': 0.85, 'valence': 0.8}

Banjo Breakdown (bluegrass, energetic) - Score: 2.46
Because: energy 0.88 vs target 0.85 (+1.47); valence 0.83 vs target 0.80 (+0.99)

Sunrise City (pop, happy) - Score: 2.45
Because: energy 0.82 vs target 0.85 (+1.47); valence 0.84 vs target 0.80 (+0.98)

Gym Hero (pop, intense) - Score: 2.29
Because: energy 0.93 vs target 0.85 (+1.30); valence 0.77 vs target 0.80 (+0.99)

Rooftop Lights (indie pop, happy) - Score: 2.25
Because: energy 0.76 vs target 0.85 (+1.25); valence 0.81 vs target 0.80 (+1.00)

Strobe Heart (edm, euphoric) - Score: 2.07
Because: energy 0.96 vs target 0.85 (+1.15); valence 0.88 vs target 0.80 (+0.92)
```

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

When changing the weights of some categories, some edge cases ended up not having any songs at all now that no songs met the criteria, or some songs ended up having way more weight due to just one trait. It still behaved simiarly but I noticed that because of the lack of dataset, users got more or less songs if they had not enough suitable songs in the databse.

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

The catalog is indeed tiny. There is no way to really tell if the song meets the criteria of the user because the dataset only has so much information. In addition, the content of the song, like how it is composed, might not agree with the user but there is no field for that.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



