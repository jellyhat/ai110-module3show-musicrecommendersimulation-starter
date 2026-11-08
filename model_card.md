# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

**Music Recommender**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

This recommender is designed for someone who has a database of songs that they would like to recommend to people who have a clear profile of their preferred genres, moods and types of songs they would like. This is also assuming the user of this can catalogue their songs well enough to describe in vague terms like mood and valence. Since it's so unrealistic for someone to be able to numerically measure songs like this, it's not really for real users but there can be real uses if used more like Pandora or Spotify.

---

## 3. How the Model Works  

The recommender works like a judge giving points. It looks at every song in the catalog one at a time, checks how well that song fits what the listener said they like, and awards points for each thing that matches. When every song has a score, it lists the songs from most points to fewest and recommends the top five.

**What it knows about each song.** Every song has a genre (like pop or lofi), a mood (like happy or chill), and a few numbers between 0 and 1 that describe how it sounds:

- **Energy:** how intense the song feels. Calm and soft is near 0, loud and driving is near 1.
- **Valence:** how happy the song sounds. Sad or dark is near 0, cheerful is near 1.
- **Acousticness:** how much it uses acoustic instruments like guitar or piano instead of electronic sounds.
- **Instrumentalness:** how likely it is to have no singing.

**What it knows about the listener.** The listener can give their favorite genres, the mood they want, how energetic and how happy they want the music to be, and optionally whether they like acoustic or instrumental music. Any preference they leave out is ignored.

**How points are awarded.**

| What's checked | Most points available |
|---|---|
| Genre is one of the listener's favorites | 1.5 (0.75 for a close genre, like "indie pop" for a pop fan) |
| Energy is close to what the listener wants | 1.5 |
| Mood matches exactly | 1.0 |
| Happiness (valence) is close to what the listener wants | 1.0 |
| Acoustic or instrumental sound fits the listener's taste | 0.5 each |

Genre and mood are simple yes-or-no checks. Energy and happiness use a sliding scale: a song that is almost exactly what the listener asked for gets nearly full points, a song that is a little off loses a few points, and a song that is far off gets close to nothing. This sliding scale follows a bell-curve shape, so small differences barely matter while big ones are punished heavily. For a listener who wants energy around 0.85, a song at 0.82 earns almost the full 1.5 points, but a sleepy song at 0.40 earns almost zero.

**Why these weights.** Genre counts the most because it reflects long-lasting taste, but only slightly more than energy, because most genres in this small catalog have just one song. A heavier genre weight let an intense rock song beat a happy indie pop song for a listener who asked for happy music. Mood and happiness together are worth more than genre alone, so the overall feel of a song can outweigh its label.

**Explaining the results.** Along with each recommendation, the system lists the reasons it earned points, such as "genre match (pop) (+1.50)" or "energy 0.82 vs target 0.85 (+1.47)". The listener can see exactly why a song made the list.

**Ties.** If two songs end up with the same score, the one listed first in the catalog wins, so the same listener always gets the same results.

**Changes from the starter logic.**

- The starter version returned the first few songs in the catalog without scoring them.
- I added a happiness (valence) preference so "happy" counts as a matter of degree, not just an exact mood label.
- I gave partial credit for closely related genres.
- Listeners can now list more than one favorite genre.
- I added an instrumentalness column to the data so listeners who want music without vocals, such as for studying, can be served.
- I left out tempo and danceability. In this dataset they mostly rise and fall with energy, so including them would count the same preference twice.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

There are twenty songs in the catalog, with a 17 different genres. I added 10 more songs with AI assistance, however there needs to be more music so that an edgecase user who likes very different songs (such as my test case EDM user) can get at least five songs listed for them. There are definitely musical tastes missing, not to mention international or songs that are not easily cataloguable.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

I think the recommender, due it's threshold limit, would not recommend songs to someone that does not match closer to their preferences. This is preferred so that a user will know both the reason and have confidence that the song is something that they have said they might enjoy. Intutitively it did not show happy songs to sad music enjoyers and vice versa, so the weights are working as intended.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

Moods are a little overrepresented, once I tried to remove mood from the weights and the song recommendations did differ a lot. However I think this demonstrates how important the weight is for mood, because it does dictate the personality of a song a lot. I think there has to be a lot more songs in the csv file, especially for the range of tastes an average person has. 

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

There were four users I tested, "Upbeat Pop/Rock", "Sad but Energetic", "Acoustic EDM Fan" and one edge case "Capitalized Input" for testing inputs. I realized the limitations of the songs.csv after the sad fan was not given a long list of songs like the upbeat pop rock fan was. This was even more seen by the EDM fan because there was only one song that matched the edm style and their mood, and what they preferred. This does make sense for the songs in the .csv but it also confirms that the recommender will not just shove the top 5 highest ranked, if they are not within a certain threshold that they will actually like.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

Definitely need more songs in the csv. It would be nice if a person could put a specific song they liked with its numerical rankings so that the system could analyze based on a song what they would like. I think also maybe if the dataset was expanded it could find songs with similar artists, that seems in real life to be a good way to find recommendations.

In addition, if the user wanted to expand their tastes they could ask the recommender to lower the threshold and show songs that are on the brink of their rankings. This is a song that they might like but would be different from that they actually like.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  


I learned about how you can adjust the weights and have widely different recommendations. However this also highlighted how important the dataset is for these types of systems. It's also a new experience to numerically weigh traits of music, a type of art that I would not normally associate with being able to objectively judge. However these numbers are needed to build an app like this and the way this app taught me is to use more qualities to weigh it on.