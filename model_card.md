# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name   

Musicure

---

## 2. Intended Use  

- What kind of recommendations does it generate?:

It generates a list of top 5 recommended songs based on user's preferences on genre, energy, mood and acoustics.

- What assumptions does it make about the user?: 

It assumes that user's know what to input to accurrately reflect their preference. The average song listener may not know what they like or how to express it numerically. It also assumes that they have just one preference instead of a range of differnet moods for different occassions.

- Is this for real users or classroom exploration?:

At the stage it is currently at, it is only for classroom exploration since it uses sample data that is both not based on real songs but also small in variety.

---

## 3. How the Model Works  

- What features of each song are used (genre, energy, mood, etc.)?:

The system looks at each song's genre (like pop, rock, jazz), mood (happy, sad, energetic), energy level (how intense or chill it is), and whether it's acoustic or electronic. These are the attributes that get matched against what a user says they like.

- What user preferences are considered?:

A user tells the recommender their favorite genre, the mood they want right now, how energetic they want the music to be (on a scale of 0 to 1), and whether they prefer acoustic instruments.

- How does the model turn those into a score?:

Does it match the genre? Does it match the mood? How close is its energy to what the user wants? Does it match their acoustic preference? The system adds up these four grades weighted by importance to give each song a final score from 0 to 1, then ranks them.

- What changes did you make from the starter logic?:

I added more songs to the data file to increase the range that it could pick from for recommendations. I then added the mathematical algorithm and then formatted the output to better present the recommended songs.

---

## 4. Data  

- How many songs are in the catalog?:

18

- What genres or moods are represented?:

pop, lofi, rock, jazz, indie, hip-hop, soul, folk, reggae, metal

- Did you add or remove data?: 

I added data to increase the pool that it could pick songs to recommend from with more variety.

- Are there parts of musical taste missing in the dataset?:  

Yes, probably need to include more classical, electronic, different cultures

---

## 5. Strengths  

Where does your system seem to work well?:

It works well in giving recommendations for the target energy level now that it weighs it more than general genre to better match the user's targetted mood. By taking other factors in consideration as well based on the algorithm, it finds recommendations that provide a well rounded fit to the user's likings. For example, Profile 4's results felt right with Neon Dreams (energetic, good energy match, wrong genre) ranked above Moonlight Sonata (correct genre, completely wrong energy), because matching how someone wants to feel matters more than matching a label.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly?:

The system does not currently consider song popularity, cultural relevance, preferred artists, or recommendations based on what other people with similar taste are also listening to. Song genres with minimal representation include classic, metal, and folk as well as general variety with different moods/energy levels associated to one genre for more range. The system seems to overfit with extremes on both sides of low/high energy because it pulls the score heavily in either direction. With the current database, it unintentionally favors popular genres like pop and lofi. It also favors users with more middle ground preferences referring back to how the extreme ends of the scale limits the songs that fit the score.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected?: 

I created 5 adversarial test profiles designed to stress the system: (1) conflicting preferences (high energy + sad mood), (2) contradictory preferences (max energy + acoustic), (3) extreme minimum energy with low acoustic preference, (4) a rare combination that doesn't exist in the dataset (classical + energetic), and (5) impossible/neutral preferences to test tiebreaking. I also tested these profiles before and after reweighting to see how much the weights mattered. I watched for whether the system gracefully degraded when preferences conflicted, whether it could rank songs sensibly when the user's stated preferences didn't match the dataset's structure, and whether extreme values (energy 0.0 or 1.0) caused scores to bottleneck or stay meaningfully spread. I also verified that scores stayed bounded between 0 and 1 and that the rankings reflected the reweighting correctly. What surprised me was the difference was made to some profiles as compared to others after reweighting. In one profile, results flipped completely where the "wrong genre" song jumped to 0.68. This showed how much genre was drowning out the other signals.

---

## 8. Future Work  

Ideas for how you would improve the model next:

The dataset already includes tempo (BPM), valence (musical positivity), and danceability, which could be added as scoring factors alongside energy and acousticness. Users could also specify artist preferences and context or activity based recommendations. Instead of just listing scores, show what factor led to the recommendation the most and why it outweighs another factor. To improve diversity, it could add a penalty to the score of similar songs if they are reduntant to increase variety. Another way to handle user preference complexity could be by learning user's behavior over time by seeing what songs they play the most, which they skip, which their friends listen to, etc.

---

## 9. Personal Reflection  

A few sentences about your experience:

Recommenders are just math with the weights you choose which can completely change which songs rank first based on percentage priority. Small tweaks to priorities cause big shifts in behavior, which is why tuning a recommender is carefully crafted and tested.

When I doubled energy's weight from 0.2 to 0.4, Profile 4's top recommendation flipped entirely where a song with the wrong genre but perfect mood and energy suddenly ranked higher than the genre match. This showed me that genre dominance was hiding how badly mismatched the energy was, and that people probably care more about how a song feels than what category it's labeled as.

Spotify and Apple Music must use way more signals than just genre, mood, and energy by probably considering artist popularity, what your friends like, what's trending, and your listening history. I also realized that the weights in any recommender are design choices that reflect the builder's opinions about what matters, which is why different apps recommend different songs for the same user.

