# Model Card: VibeFinder 1.0

## 1. Model Name

**VibeFinder 1.0** — a content-based music recommender simulation.

---

## 2. Intended Use

VibeFinder is designed to suggest songs from a small catalog based on a user's stated genre preference, mood preference, and target energy level.

- It is intended for **classroom exploration** of how real recommendation systems work — not for production use.
- It assumes the user can describe their current mood and energy preference explicitly. It does not learn from listening history.
- It should **not** be used to make real product decisions, gate content, or influence what music a real user sees on a live platform. The catalog is too small and the algorithm too simple for any of that.

---

## 3. How the Model Works

VibeFinder gives every song a numeric score based on how closely it matches what the user wants, then returns the top-ranked songs.

The scoring works like this:

- If the song's genre is the same as the user's favorite genre, it gets **+2 points**. Genre is the strongest signal.
- If the song's mood matches the user's preferred mood, it gets **+1 point**.
- The system measures how close the song's energy level (a 0-to-1 scale) is to the user's target energy. A perfect match adds **up to +1.5 points**; a big difference adds almost nothing.
- Optionally, valence (musical positivity) proximity can add **up to +0.5 points**.

Once every song has a score, the list is sorted highest-to-lowest and the top 5 are returned along with the breakdown of why each was chosen.

Think of it as a judge at a talent show marking a scorecard: genre is worth the most, mood is second, and energy fit decides ties.

---

## 4. Data

- **Catalog size**: 20 songs.
- **Features per song**: genre, mood, energy (0–1), tempo_bpm, valence (0–1), danceability (0–1), acousticness (0–1).
- **Genres represented**: pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip hop, country, EDM, R&B, metal, classical, latin, emo, blues, chiptune.
- **Moods represented**: happy, chill, intense, relaxed, focused, moody, energetic, nostalgic, euphoric, romantic, peaceful, festive, sad, melancholic, playful.

**Added data**: 10 songs were added beyond the starter 10 to include a more diverse range of genres (metal, blues, classical, EDM, etc.) and moods (melancholic, euphoric, peaceful, festive) that were missing from the original dataset.

**What's missing**: The dataset has no songs in styles like K-pop, reggae, gospel, or bossa nova. It also has no metadata about language, decade of release, or explicit content — things a real recommender would use. Every genre appears at most twice, which limits variety for any user outside of pop or lofi.

---

## 5. Strengths

- **Pop and lofi users get strong recommendations**: These genres have 2–3 songs each, so the system can rank within the genre by mood and energy rather than just returning a single match.
- **The scoring is fully transparent**: Every recommendation comes with a "because" explanation in plain English. A user always knows why a song ranked where it did.
- **Energy proximity works well for genre-crossover cases**: A "pop/happy" user who also likes the energy of synthwave will see "Night Drive Loop" in the top 5, because its energy (0.75) is close to the target (0.80). This is a reasonable suggestion even though the genre doesn't match.

---

## 6. Limitations and Bias

**Filter bubble by genre**: Genre carries +2.0 points and is an exact string match. Any user whose favorite genre appears once in the catalog gets one great recommendation and then four mediocre energy-only fillers. Blues, metal, classical, and chiptune each have exactly one song.

**Pop overrepresentation**: Pop songs (Sunrise City, Gym Hero, Rooftop Lights) appear in nearly every profile's top-5 because their energy values (0.76–0.93) happen to be close to many users' targets. A "Deep Blues Listener" still gets pop songs ranked 4–5 not because they like pop, but because the energy numbers line up. This is a classic filter bubble caused by an imbalanced dataset.

**Mood is binary**: The system gives +1 for an exact mood match and +0 for everything else. A user who wants "relaxed" gets nothing from a "chill" song even though those moods are close. A real system would use a similarity metric between moods rather than exact matching.

**Energy dominance for niche genres**: When genre and mood both miss (as they often do for EDM, metal, or blues users after rank #1), the only tie-breaker is energy proximity. This means ranks 2–5 for niche genre users are essentially random and not meaningful.

**No listening context**: The system has no idea if the user is at the gym, studying, or relaxing. The same profile always gets the same list regardless of time of day or context.

---

## 7. Evaluation

**Profiles tested**:

1. **Happy Pop Fan** (genre=pop, mood=happy, energy=0.80) — Results felt right. Sunrise City ranked #1 (the only pop/happy song), Gym Hero #2 (pop but intense). Rooftop Lights at #3 is indie pop/happy which is close — the system can't see the "indie" prefix so it missed the match.

2. **Chill Lofi Studier** (genre=lofi, mood=chill, energy=0.40) — Best results of all profiles. Three lofi songs in the catalog, two with chill mood. The ranking within the lofi/chill cluster (Midnight Coding vs Library Rain) was decided by tiny energy differences — plausible.

3. **High-Energy EDM** (genre=edm, mood=euphoric, energy=0.95) — Only one EDM song. After rank #1 the system returns metal, pop, and rock songs based purely on high energy. These are genre-inappropriate even if energetically similar. The EDM profile exposed the genre-cliff problem most clearly.

4. **Deep Blues Listener** (genre=blues, mood=melancholic, energy=0.45) — Same problem as EDM. Delta Blues is a perfect match at rank #1, then ranks 2–5 are lofi/jazz songs that happen to sit near 0.45 energy. Reasonable as "calm" alternatives but not blues.

5. **Intense Metalhead** (genre=metal, mood=intense, energy=0.95) — Iron Thunder is the clear #1. Gym Hero and Storm Runner at ranks 2–3 share the "intense" mood which is a meaningful signal — the system correctly identified mood overlap even across genre boundaries.

**Comparison: EDM vs Metalhead** — Both profiles want high energy (~0.95), but their results diverge after rank #1 because the Metalhead profile gets two "intense" mood matches (Gym Hero, Storm Runner) while the EDM profile gets nothing in the mood column. The Metalhead profile is noticeably more useful at ranks 2–3 purely because "intense" mood appears 3 times in the catalog while "euphoric" appears only once.

**Comparison: Pop Fan vs Blues Listener** — The Pop Fan gets 3 songs with at least one matching dimension (genre or mood) in the top 5. The Blues Listener gets only 1. This difference is entirely a dataset imbalance issue, not a flaw in the algorithm.

**Surprise**: The "Rooftop Lights" miss (genre stored as "indie pop" not "pop") revealed that genre matching is brittle. A user who types "pop" will never match "indie pop" even though the songs feel similar. This would never happen in a real system, which would use genre hierarchies or embeddings.

---

## 8. Future Work

1. **Expand the catalog to at least 100 songs per genre** — The single biggest improvement. Genre-cliff problems disappear when there are 10 metal songs to rank by mood and energy rather than just one.

2. **Replace exact mood matching with mood similarity groups** — Group related moods ("chill," "relaxed," "peaceful," "focused") so a chill user gets partial credit from a relaxed song. A simple lookup table or mood graph would work.

3. **Add a diversity penalty** — If the top 5 are all from the same artist or genre, apply a small score reduction to songs 3–5 that repeat the same genre. This would push variety into the lower slots without breaking the top 2 results.

4. **Incorporate danceability and tempo proximity** — Both features are in the dataset but ignored by the scorer. A dance-oriented user should rank "Samba Dreams" higher than "Midnight Coding" even if energy is similar.

5. **Hybrid filtering** — Combine content scores with collaborative signals (e.g., "users with this profile also saved these tracks") once the user base is large enough. Pure content-based systems plateau quickly; collaborative signals unlock genre-crossing discovery.

---

## 9. Personal Reflection

**What I learned**: Building this system made it obvious that a recommendation is not really "intelligence" — it is just a weighted lookup. The surprising part is that it still *feels* like a recommendation when it works. When Sunrise City ranked first for a pop/happy user, the result made intuitive sense even though the math was just arithmetic on a spreadsheet. Real platforms are doing the same thing at vastly larger scale, with hundreds of features and millions of songs, but the core idea is identical.

**How AI tools helped**: I used AI to brainstorm the scoring formula and choose feature weights. The suggestion to use `1.5 × (1 − |gap|)` for energy proximity (rewarding closeness rather than absolute value) was a key design insight I might have missed. I had to verify by running the scorer manually on a few songs to confirm the formula behaved as expected — the AI got the math right but I had to check that the *interpretation* was correct (closer is better, not higher is better).

**What surprised me**: How quickly genre imbalance creates unfair results. I assumed 20 diverse songs would be enough, but niche genre users (EDM, blues, metal) get one good recommendation and then four generic ones. The algorithm is not biased in the sense of being wrong — it is doing exactly what it was told. The bias lives in the dataset, not the code.

**What I would try next**: I would add a mood-similarity matrix so "chill" users get partial credit from "relaxed" and "peaceful" songs. That single change would probably improve the perceived quality of recommendations more than any weight adjustment.
