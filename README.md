# Music Recommender Simulation

## Project Summary

This project builds a content-based music recommender in Python. Given a user's genre preference, favorite mood, and target energy level, the system scores every song in a catalog and returns the best matches in ranked order — along with a plain-language explanation of why each song was chosen.

This mirrors how real platforms like Spotify use song attributes (not social data) to suggest tracks. The simulation keeps the math transparent so you can see exactly how each score is calculated.

---

## How The System Works

### Real-world context

Major streaming platforms use two main strategies to recommend music:

- **Collaborative filtering** — "users who liked the same songs as you also liked these." It learns from patterns in millions of listeners' behavior (plays, skips, saves) without knowing anything about the songs themselves.
- **Content-based filtering** — "this song has the same attributes as songs you already like." It looks at measurable features of each track (tempo, energy, genre, mood) and recommends songs that are similar to the user's stated preferences.

This simulation uses content-based filtering because the math is fully visible and easy to reason about.

### Song features used

Each `Song` object stores:

| Feature | Type | Description |
|---|---|---|
| `genre` | string | Musical genre (pop, lofi, metal, etc.) |
| `mood` | string | Emotional tone (happy, chill, intense, etc.) |
| `energy` | float 0–1 | Perceived intensity and activity level |
| `tempo_bpm` | float | Beats per minute |
| `valence` | float 0–1 | Musical positiveness (high = upbeat) |
| `danceability` | float 0–1 | How suitable the track is for dancing |
| `acousticness` | float 0–1 | Confidence that the track is acoustic |

### User profile

A `UserProfile` stores:

| Preference | Type |
|---|---|
| `favorite_genre` | string |
| `favorite_mood` | string |
| `target_energy` | float 0–1 |
| `likes_acoustic` | bool |

The functional API (`recommend_songs`) accepts a dict with `genre`, `mood`, and `energy` keys. Optional keys `valence` and `likes_acoustic` unlock additional scoring dimensions.

### Algorithm Recipe

For every song in the catalog the system computes a score using these weighted rules:

| Rule | Points | Notes |
|---|---|---|
| Genre match | +2.0 | Exact string match |
| Mood match | +1.0 | Exact string match |
| Energy proximity | 0 – +1.5 | `1.5 × (1 − |user_energy − song_energy|)` |
| Valence proximity *(optional)* | 0 – +0.5 | `0.5 × (1 − |user_valence − song_valence|)` |
| Acoustic preference *(OOP only)* | +0.5 / +0.3 | Bonus when acoustic taste matches song's acousticness |

Genre carries the most weight (2×) because genre is the strongest signal of musical taste. Energy uses a proximity formula so songs that are *close* to your target score higher than songs that are merely high or low — a runner wanting energy 0.8 should see "Sunrise City" above "Iron Thunder."

### Ranking rule

`recommend_songs` loops over every song, scores it, then calls `sorted()` to produce a new list ordered highest-score-first. `sorted()` is used rather than `.sort()` because it returns a fresh list and leaves the original catalog untouched, which matters if you call the function multiple times with different profiles.

### Data flow

```
User Preferences (dict)
        │
        ▼
for each Song in catalog:
    score, reasons = score_song(user_prefs, song)
        │
        ▼
sorted by score (descending)
        │
        ▼
Top K  →  (song, score, explanation)
```

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   python -m src.main
   ```

### Running Tests

```bash
pytest
```

---

## Sample Recommendation Output

```
Loaded songs: 20

====================================================
Profile : Happy Pop Fan
Prefs   : genre=pop, mood=happy, energy=0.8
====================================================
  1. Sunrise City — Neon Echo
     Score: 4.47  |  genre match: pop (+2.0), mood match: happy (+1.0), energy proximity (+1.47)
  2. Gym Hero — Max Pulse
     Score: 3.30  |  genre match: pop (+2.0), energy proximity (+1.30)
  3. Rooftop Lights — Indigo Parade
     Score: 2.44  |  mood match: happy (+1.0), energy proximity (+1.44)
  4. Samba Dreams — Rio Colors
     Score: 1.48  |  energy proximity (+1.48)
  5. Night Drive Loop — Neon Echo
     Score: 1.42  |  energy proximity (+1.42)

====================================================
Profile : Chill Lofi Studier
Prefs   : genre=lofi, mood=chill, energy=0.4
====================================================
  1. Midnight Coding — LoRoom
     Score: 4.47  |  genre match: lofi (+2.0), mood match: chill (+1.0), energy proximity (+1.47)
  2. Library Rain — Paper Lanterns
     Score: 4.42  |  genre match: lofi (+2.0), mood match: chill (+1.0), energy proximity (+1.42)
  3. Focus Flow — LoRoom
     Score: 3.50  |  genre match: lofi (+2.0), energy proximity (+1.50)
  4. Spacewalk Thoughts — Orbit Bloom
     Score: 2.32  |  mood match: chill (+1.0), energy proximity (+1.32)
  5. Coffee Shop Stories — Slow Stereo
     Score: 1.46  |  energy proximity (+1.46)

====================================================
Profile : High-Energy EDM
Prefs   : genre=edm, mood=euphoric, energy=0.95
====================================================
  1. Neon Pulse — Synthwave X
     Score: 4.48  |  genre match: edm (+2.0), mood match: euphoric (+1.0), energy proximity (+1.48)
  2. Iron Thunder — Voltage
     Score: 1.50  |  energy proximity (+1.50)
  3. Gym Hero — Max Pulse
     Score: 1.47  |  energy proximity (+1.47)
  4. Storm Runner — Voltline
     Score: 1.44  |  energy proximity (+1.44)
  5. Trap Kings — Blaze & Dre
     Score: 1.38  |  energy proximity (+1.38)

====================================================
Profile : Deep Blues Listener
Prefs   : genre=blues, mood=melancholic, energy=0.45
====================================================
  1. Delta Blues — River Muddy
     Score: 4.47  |  genre match: blues (+2.0), mood match: melancholic (+1.0), energy proximity (+1.47)
  2. Midnight Coding — LoRoom
     Score: 1.46  |  energy proximity (+1.46)
  3. Focus Flow — LoRoom
     Score: 1.42  |  energy proximity (+1.42)
  4. Coffee Shop Stories — Slow Stereo
     Score: 1.38  |  energy proximity (+1.38)
  5. Blue Ridge Road — The Wayfarers
     Score: 1.36  |  energy proximity (+1.36)

====================================================
Profile : Intense Metalhead
Prefs   : genre=metal, mood=intense, energy=0.95
====================================================
  1. Iron Thunder — Voltage
     Score: 4.50  |  genre match: metal (+2.0), mood match: intense (+1.0), energy proximity (+1.50)
  2. Gym Hero — Max Pulse
     Score: 2.47  |  mood match: intense (+1.0), energy proximity (+1.47)
  3. Storm Runner — Voltline
     Score: 2.44  |  mood match: intense (+1.0), energy proximity (+1.44)
  4. Neon Pulse — Synthwave X
     Score: 1.48  |  energy proximity (+1.48)
  5. Trap Kings — Blaze & Dre
     Score: 1.38  |  energy proximity (+1.38)
```

---

## Experiments You Tried

### Weight shift: doubling energy, halving genre

When genre weight was cut from 2.0 to 1.0 and energy weight raised from 1.5 to 3.0, the "Happy Pop Fan" profile dropped "Gym Hero" (pop/intense) and elevated "Samba Dreams" (latin/festive) because its energy (0.81) is marginally closer to 0.8. This shows the system is sensitive to weight changes — genre identity matters less than pure vibe when genre weight drops.

### Feature removal: removing mood

Commenting out the mood check made the "Intense Metalhead" profile rank "Neon Pulse" (EDM, euphoric) equal to "Storm Runner" (rock, intense) because both share similar energy levels. Without mood, the system can't distinguish "intense" from "euphoric," which feels wrong and proves that mood adds real signal even at only +1.0 points.

### Edge-case profile: conflicting preferences (energy=0.95, mood=sad)

```
Profile : Conflicted Listener
Prefs   : genre=emo, mood=sad, energy=0.95
  1. Broken Signal — The Lows  (emo/sad — genre + mood match dominate)
  2. Iron Thunder — Voltage    (high energy, no mood/genre match)
  3. Neon Pulse — Synthwave X  (high energy, no mood/genre match)
```

The system resolved the conflict by giving the exact-genre-and-mood match a combined bonus of +3.0 that overwhelmed the energy gap. Songs ranked 2–5 were pure energy matches with no mood alignment — which is probably *not* what a sad listener wants.

---

## Limitations and Risks

- The catalog has only 20 songs, so recommendations 4–5 are often weak energy-only matches with no genre or mood alignment.
- Genre uniqueness: each rare genre (blues, metal, classical, chiptune) has exactly one song, so those users get a perfect #1 then fall off a cliff in quality.
- The scoring does not consider tempo, danceability, or valence by default — two very different "pop/happy" songs can look identical to the system.
- Acoustic preference only affects the OOP `Recommender` class; the functional `recommend_songs` path ignores it unless `valence` is added to the prefs dict.

See `model_card.md` for a deeper analysis.

---

## Reflection

See [Model Card](model_card.md) for a full reflection and bias analysis.

The biggest surprise was how quickly the system creates a "genre cliff": if your genre appears only once in the catalog, you get one great match and then four mediocre energy-only matches. Real systems solve this with much larger catalogs and collaborative filtering to cross genre boundaries. Even a simple weighted formula can feel like a recommendation — but it is really just a lookup with math attached.
