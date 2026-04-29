# PawPal+ (Module 2 Project)
PawPal+ is a Streamlit-based assistant designed to help busy pet owners generate and explain optimized daily care schedules based on specific constraints like time and priority. To build it, you will first design the system architecture (UML), implement the core scheduling logic and unit tests in Python, and finally integrate everything into a functional UI.


## Title & Summary
PawPal+ is an AI-powered pet care scheduling assistant that generates personalized daily task plans based on a pet's species, breed, and age, as well as how much time the owner has available. Many pet owners do not know what their specific pet truly needs to stay healthy, and looking up care guidelines for every breed is time-consuming. PawPal+ solves this by automatically retrieving real veterinary guidelines from trusted sources and turning them into a clear, prioritized schedule with sourced reasoning for each task. It matters because proper daily care, like the right amount of exercise, feeding frequency, and grooming, directly affects a pet's health and wellbeing, and making that information easy to act on helps owners do better for their pets every day.

### Architecture Overview
The user enters their pet's name, species, breed, age, and daily availability. The system searches trusted vet websites (AKC, ASPCA, VCA, PDSA) using the You.com API for breed-specific guidelines, and also pulls from a built-in knowledge base of 20 vet-sourced documents. A RAG retriever finds the most relevant content using semantic search. That context is used to build a task list where each task includes a start time, duration, priority, and a sourced reason pulled from the vet documents. The schedule is then sorted by priority and time, checked for conflicts, and displayed in the Streamlit UI.


## Setup Instructions

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Create a `.env` file in the project root (optional — app works without it):
   ```
   YOU_API_KEY=your_key
   ```
3. Run the app:
   ```
   streamlit run app.py
   ```




## Sample Interactions

**Example 1 — Dog, Golden Retriever, 5 years**
- 🔴 Feed — 08:00 · 10 min · *"Dogs should be fed twice daily, spaced 8–12 hours apart (ASPCA). Measure portions carefully — 57% of dogs in the U.S. are overweight."*
- 🔴 Exercise — 09:00 · 30 min · *"Regular exercise keeps Golden Retriever dogs healthy — consult your vet for breed-specific duration (VCA, American Humane)."*
- 🟡 Walk — 17:00 · 15 min · *"A second daily walk helps meet the recommended 1–2 walks per day guideline (PDSA). In hot weather, walk during cooler morning or evening hours."*
- 🟡 Play — 15:00 · 20 min · *"Interactive play like hide-and-seek, fetch, and puzzle feeders provides mental stimulation alongside physical activity."*
- 🟡 Dental Care — 19:00 · 5 min · *"Most pets show signs of dental disease by age 3, making daily brushing essential (Gardens Animal Hospital)."*
- 🟢 Groom — 19:30 · 15 min · *"Regular grooming for Golden Retriever dogs reduces shedding and lets you check for skin issues (ASPCA, OVRS)."*

**Example 2 — Cat, Persian, 2 years**
- 🔴 Feed — 08:00 · 5 min · *"Feed a high-quality diet suited to your Persian cat's age and health needs (ASPCA). 60% of cats in the U.S. are overweight."*
- 🔴 Litter Box — 08:30 · 5 min · *"Scoop at least once daily — cats avoid dirty boxes which can cause stress and health issues (ASPCA)."*
- 🟡 Morning Play — 10:00 · 10 min · *"Regular exercise keeps Persian cats healthy — use wand toys or laser pointers to encourage movement (VCA, American Humane)."*
- 🟡 Evening Play — 17:00 · 10 min · *"A second play session mirrors a cat's natural hunting pattern of dawn and dusk activity (American Humane)."*
- 🟡 Dental Care — 19:00 · 5 min · *"Most cats show signs of dental disease by age 3, but cats often hide pain making prevention critical (Gardens Animal Hospital)."*
- 🟢 Groom — 19:30 · 10 min · *"Regular grooming for Persian cats reduces shedding and lets you check for skin issues (ASPCA, OVRS)."*

**Example 3 — Rabbit, Holland Lop, 1 year**
- 🔴 Feed — 08:00 · 10 min · *"Feed a high-quality diet suited to your Holland Lop rabbit's age and health needs (ASPCA). Always provide fresh hay and water."*
- 🟡 Playtime — 10:00 · 15 min · *"Regular exercise keeps Holland Lop rabbits healthy — consult your vet for breed-specific duration (VCA, American Humane)."*
- 🟡 Exercise — 14:00 · 30 min · *"Rabbits need regular free-roaming time daily for physical and mental health (VCA, American Humane)."*
- 🟢 Groom — 19:00 · 10 min · *"Regular grooming for Holland Lop rabbits reduces shedding and lets you check for skin issues (ASPCA, OVRS)."*



## Design Decisions

We built the system this way to provide trustworthy, relevant content that is real-time and specific to the user's pet. Instead of hardcoding generic tasks, the system retrieves actual veterinary guidelines based on the exact species, breed, and age the user enters — so a Golden Retriever gets different recommendations than a Chihuahua, and a rabbit gets different recommendations than a cat. The You.com Search API uses the user's species and breed as the search query, then filters results by topic keywords like "exercise", "feed", and "groom" so only medically relevant snippets are kept — not ads or unrelated content. Results are also limited to trusted vet domains (AKC, ASPCA, VCA, PDSA) and one result per website to keep sources diverse and credible. A confidence scorer was added so users always know how reliable the output is. The trade-off is that very rare breeds may return fewer live results, but accurate over abundant was the priority.




## Testing Summary

The system was tested across four methods. Automated unit tests verified that the retriever, fallback recommender, confidence scorer, and error handling all work correctly across different species, ages, and missing inputs. Confidence scores averaged 0.65 for fallback-only output and rose above 0.8 when breed-specific data was found, confirming the scorer correctly reflects output quality. Logging captured every API failure and fallback trigger so errors were traceable without crashing the app. Human evaluation output was reviewed for dog, cat, and rabbit samples to confirm tasks were relevant, prioritized correctly, and included sourced reasoning.

What worked was the fallback system and the You.com retrieval pipeline — together they produced reliable, cited recommendations even without a working AI language model. What didn't work was connecting to Gemini or OpenAI directly, as both hit API access issues like rate limits, quota errors, and authentication failures, meaning LLM-generated schedules could not run. This is a feature that could be added in the future with proper API credits. Even the You.com API initially returned irrelevant content like ad snippets and duplicate results from the same site, because the search query alone was not enough to guarantee quality. This was fixed by adding topic keyword filtering and limiting results to one per trusted vet domain. What I learned is that RAG does not have to mean an LLM — in this case, You.com acted as the retrieval layer, pulling real-time vet content and feeding it into the system to generate recommendations, which showed that retrieval technology can automate research that would otherwise require manually browsing dozens of websites.


## Reflection

This project taught me that AI models are flawed and require constant testing to catch and debug issues. You have to build tests, run them, go back into the code, filter and tune it in the right direction, and repeat until the output is actually reliable. Building a useful AI system is also mostly about the data around it, not the model itself. The recommendations only became trustworthy once the retrieval was grounded in real vet sources with proper filtering. It also showed how important reliability is because an app that crashes when an API is unavailable is not useful, so the fallback system was just as important to build as the main pipeline.



