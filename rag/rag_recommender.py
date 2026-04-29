"""
RAG Task Recommender
Uses Claude API with retrieved pet care knowledge to recommend tasks for pets.
Combines simple prompt-based approach with semantic search for context.
"""

import json
import os
import re
import requests
from typing import List, Optional
from pawpal_system import Task, Pet
from rag.pet_care_kb import PetCareRetriever


class RAGTaskRecommender:
    """
    Task Recommender powered by RAG.
    Retrieves relevant pet care knowledge and uses Claude to generate task recommendations.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize recommender with Gemini API and knowledge retriever.

        Args:
            api_key: Gemini API key. If None, will use GEMINI_API_KEY env var.
        """
        self.retriever = PetCareRetriever()
        self.api_key = api_key or os.getenv("OPEN_AI_API_KEY")
        self.client = None
        self._initialize_client()

    def _initialize_client(self):
        """Initialize OpenAI client if API key is available."""
        if self.api_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
            except Exception:
                self.client = None
    
    def _retrieve_context(self, pet: Pet, topic: str) -> str:
        """
        Retrieve relevant knowledge for task recommendation.
        
        Args:
            pet: Pet object with species and age
            topic: What tasks we're recommending for
            
        Returns:
            Relevant context from knowledge base
        """
        return self.retriever.retrieve(
            pet_species=pet.species.lower(),
            pet_age=pet.age,
            query_topic=topic
        )
    
    def _search_breed_guidelines(self, breed: str, species: str) -> dict:
        """
        Search You.com API for breed-specific care guidelines.
        Returns dict with topics as keys and snippet text as values.
        """
        you_key = os.getenv("YOU_API_KEY", "").strip()
        if not you_key or not breed:
            return {}

        topics = {
            "exercise": f"{breed} {species} exercise how much daily minutes",
            "grooming": f"{breed} {species} grooming frequency brushing",
            "feeding":  f"{breed} {species} feeding diet nutrition",
        }
        trusted_domains = (
            "vcahospitals.com,aspca.org,akc.org,avma.org,vet.cornell.edu,"
            "petmd.com,humanesociety.org,rspca.org.uk,pdsa.org.uk,"
            "aaha.org,bluepearlvet.com,banfield.com,merckvetmanual.com,"
            "peteducation.com,whole-dog-journal.com,catvets.com"
        )

        # Keywords that must appear in a snippet for it to count as relevant
        topic_keywords = {
            "exercise": ["exercise", "walk", "activity", "play", "run", "active", "minute", "hour"],
            "grooming": ["groom", "brush", "coat", "fur", "trim", "shed", "bathe", "nail", "hair"],
            "feeding":  ["feed", "food", "diet", "nutrition", "meal", "eat", "calori", "protein"],
        }

        results = {}
        for topic, query in topics.items():
            try:
                resp = requests.get(
                    "https://ydc-index.io/v1/search",
                    headers={"X-API-Key": you_key},
                    params={
                        "query": f"{query} veterinary care guidelines",
                        "count": 3,
                        "include_domains": trusted_domains,
                    },
                    timeout=5,
                )
                hits = resp.json().get("results", {}).get("web", [])
                keywords = topic_keywords.get(topic, [])
                snippets = []
                seen_domains = set()
                for hit in hits:
                    url = hit.get("url", "")
                    domain = url.split("/")[2] if url else ""
                    if domain in seen_domains:
                        continue
                    for s in hit.get("snippets", [])[:3]:
                        s = s.strip()
                        if s and any(kw in s.lower() for kw in keywords):
                            snippets.append(f"(Source: {url}) {s}")
                            seen_domains.add(domain)
                            break
                results[topic] = " ".join(snippets)
            except Exception:
                results[topic] = ""
        return results

    def _extract_duration(self, text: str, default: int) -> int:
        """Parse the first plausible exercise duration (minutes) from snippet text."""
        # Look for patterns like "60 minutes", "1-2 hours", "30 to 60 minutes"
        hours = re.findall(r'(\d+(?:\.\d+)?)\s*(?:to\s*\d+)?\s*hour', text, re.IGNORECASE)
        mins  = re.findall(r'(\d+)\s*(?:to\s*(\d+))?\s*minute', text, re.IGNORECASE)
        if hours:
            return min(int(float(hours[0]) * 60), 120)
        if mins:
            lo = int(mins[0][0])
            hi = int(mins[0][1]) if mins[0][1] else lo
            return min((lo + hi) // 2, 120)
        return default

    def recommend_tasks(self, pet: Pet, owner_constraints: Optional[str] = None) -> List[dict]:
        """
        Generate task recommendations for a pet using RAG.
        
        Args:
            pet: Pet object to recommend tasks for
            owner_constraints: Optional string about owner's availability/preferences
            
        Returns:
            List of recommended tasks with reasoning from research
        """
        if not self.client:
            return self._fallback_recommendations(pet)
        
        # Build species/breed/age-specific topics alongside general ones
        breed = getattr(pet, "breed", "") or ""
        age_stage = (
            "puppy" if pet.age < 1 else
            "senior" if pet.age >= 7 else
            "adult"
        )
        topics_to_retrieve = [
            "feeding", "exercise", "grooming", "training",
            "play", "dental care", "hydration", "enrichment",
            "wellness routine", "weight management",
            f"{pet.species} care",
            f"{age_stage} {pet.species} care",
        ]
        if breed:
            topics_to_retrieve.append(f"{breed} {pet.species} exercise grooming")

        # Live breed-specific search via You.com API
        breed_guidelines = self._search_breed_guidelines(breed, pet.species)

        contexts = {
            topic: self._retrieve_context(pet, topic)
            for topic in topics_to_retrieve
        }
        # Merge live breed search results into contexts
        for topic, content in breed_guidelines.items():
            if content:
                contexts[f"{breed} {topic}"] = content

        # Build prompt with retrieved context
        prompt = self._build_prompt(pet, contexts, owner_constraints)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1024,
            )
            response_text = response.choices[0].message.content
        except Exception as e:
            error_str = str(e)
            if any(kw in error_str for kw in ["429", "401", "quota", "rate", "auth", "invalid_api_key"]):
                self._rate_limit_message = "API unavailable — showing built-in recommendations instead."
                return self._fallback_recommendations(pet)
            raise

        tasks = self._parse_recommendations(response_text, pet)
        return tasks
    
    def _build_prompt(self, pet: Pet, contexts: dict, constraints: Optional[str] = None) -> str:
        """
        Build prompt for Claude with retrieved context.
        
        Args:
            pet: Pet to recommend tasks for
            contexts: Dict of retrieved knowledge by topic
            constraints: Owner's time/preference constraints
            
        Returns:
            Prompt for Claude API
        """
        age_stage = (
            "puppy" if pet.age < 1 else
            "senior" if pet.age >= 7 else
            "adult"
        )
        all_context = "\n\n".join(
            f"[{topic.upper()}]\n{content}"
            for topic, content in contexts.items()
            if content.strip()
        )

        prompt = f"""
You are a veterinary-informed pet care expert recommending a personalized daily schedule for a pet owner.

PET INFORMATION:
- Name: {pet.name}
- Species: {pet.species}
- Breed: {getattr(pet, "breed", "") or "unspecified"}
- Age: {pet.age} years old (life stage: {age_stage})
{"- " + constraints if constraints else ""}

KNOWLEDGE BASE (Retrieved from veterinary sources, animal hospitals, and pet care organizations):
{all_context}

TASK:
Using the knowledge base above, recommend 5-8 essential daily tasks for {pet.name} the {pet.species}.
Personalize the tasks based on the pet's age, species, and any owner constraints provided.
For each task, write a 1-2 sentence reasoning that explains WHY this task matters, citing the source guidelines.

Return ONLY a JSON array in this exact format, no extra text:
[
  {{
    "name": "Task Name",
    "priority": "high|medium|low",
    "duration": 20,
    "start_time": "08:00",
    "recurrence": "daily|weekly|monthly",
    "reasoning": "1-2 sentences explaining why this task is important for this specific pet, citing the source."
  }}
]
"""
        return prompt
    
    def _parse_recommendations(self, response_text: str, pet: Pet) -> List[Task]:
        """
        Parse Claude's JSON response into Task objects.
        
        Args:
            response_text: Claude's JSON response
            pet: Pet to attach tasks to
            
        Returns:
            List of Task objects with reasoning stored as description
        """
        tasks = []
        
        try:
            # Extract JSON from response
            json_str = response_text.strip()
            recommendations = json.loads(json_str)
            
            for rec in recommendations:
                task = Task(
                    name=rec.get("name", "Unnamed Task"),
                    priority=rec.get("priority", "medium"),
                    duration=rec.get("duration", 15),
                    start_time=rec.get("start_time", "08:00"),
                    recurrence=rec.get("recurrence", "daily")
                )
                
                # Store reasoning as metadata (can extend Task class if needed)
                task.reasoning = rec.get("reasoning", "")
                
                tasks.append(task)
        
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Error parsing recommendations: {e}")
            return self._fallback_recommendations(pet)
        
        return tasks
    
    def score_confidence(self, tasks: List[Task], used_ai: bool, breed_data_found: bool) -> dict:
        """
        Rate confidence in the recommendations on a 0-1 scale.
        Returns a dict with overall score and per-factor breakdown.
        """
        scores = {}

        # Factor 1: did the AI generate these or is it fallback?
        scores["ai_generated"] = 1.0 if used_ai else 0.4

        # Factor 2: do tasks have sourced reasoning?
        tasks_with_reasoning = sum(1 for t in tasks if getattr(t, "reasoning", ""))
        scores["has_reasoning"] = tasks_with_reasoning / len(tasks) if tasks else 0.0

        # Factor 3: were breed-specific sources found?
        scores["breed_specific"] = 1.0 if breed_data_found else 0.5

        # Factor 4: are durations in a sane range?
        reasonable = sum(1 for t in tasks if 1 <= t.duration <= 120)
        scores["duration_sanity"] = reasonable / len(tasks) if tasks else 0.0

        # Factor 5: do we have high-priority essential tasks (feeding)?
        has_feed = any("feed" in t.name.lower() for t in tasks)
        scores["has_essentials"] = 1.0 if has_feed else 0.3

        overall = sum(scores.values()) / len(scores)
        scores["overall"] = round(overall, 2)
        return scores

    def _fallback_recommendations(self, pet: Pet) -> List[Task]:
        """
        Fallback recommendations when API is unavailable.
        Uses the knowledge base to attach real sourced reasoning to each task.

        Args:
            pet: Pet to recommend tasks for

        Returns:
            List of task recommendations with KB-sourced reasoning
        """
        species = pet.species.lower()
        age = pet.age
        breed = (getattr(pet, "breed", "") or "").strip()

        # Search You.com for breed/species-specific guidelines for ANY species the user enters
        search_term = breed if breed else species
        breed_data = self._search_breed_guidelines(search_term, species)
        exercise_text = breed_data.get("exercise", "")
        grooming_text = breed_data.get("grooming", "")
        feeding_text  = breed_data.get("feeding", "")

        label = f"{breed} {species}".strip() if breed else species

        # Extract durations from real search results, fall back to sensible defaults
        exercise_duration = self._extract_duration(exercise_text, default=30)
        walk_duration     = max(10, exercise_duration // 2)

        exercise_note = (
            f"Based on search results for {label}: " + " ".join(exercise_text.split()[:30]) + "..."
            if exercise_text else
            f"Regular exercise keeps {label}s healthy — consult your vet for breed-specific duration (VCA, American Humane)."
        )
        groom_note = (
            f"Based on search results for {label}: " + " ".join(grooming_text.split()[:30]) + "..."
            if grooming_text else
            f"Regular grooming for {label}s reduces shedding and lets you check for skin issues (ASPCA, OVRS)."
        )
        feed_note = (
            f"Based on search results for {label}: " + " ".join(feeding_text.split()[:30]) + "..."
            if feeding_text else
            f"Feed a high-quality diet suited to your {label}'s age and health needs (ASPCA, FPC Vets)."
        )

        if species == "dog":
            age_note = "puppy" if age < 1 else ("senior" if age >= 7 else "adult")
            raw_tasks = [
                (
                    "Feed", "high", 10, "08:00", "daily",
                    f"Dogs should be fed twice daily, spaced 8–12 hours apart (ASPCA). "
                    f"{'Puppies need 3–4 meals daily with 25–30% protein for healthy growth.' if age_note == 'puppy' else 'Senior dogs may need a breed-appropriate senior diet starting at age 6–7.' if age_note == 'senior' else 'Measure portions carefully — 57% of dogs in the U.S. are overweight (NaturVet).'}"
                ),
                (
                    "Exercise", "high", exercise_duration, "09:00", "daily",
                    exercise_note +
                    f" {'Short play spurts are better than long runs for puppies to protect growing joints (VCA).' if age_note == 'puppy' else 'Senior dogs benefit from shorter, gentler uphill walks to maintain strength (Dr. Dobias).' if age_note == 'senior' else ''}"
                ),
                (
                    "Walk", "medium", walk_duration, "17:00", "daily",
                    "A second daily walk helps meet the recommended 1–2 walks per day guideline (PDSA). "
                    "In hot weather, walk during cooler morning or evening hours to prevent heatstroke (PDSA, VCA)."
                ),
                (
                    "Play", "medium", 20, "15:00", "daily",
                    "Interactive play like hide-and-seek, fetch, and puzzle feeders provides mental stimulation alongside physical activity (Hill's Pet, OVRS). "
                    "Avoid repetitive ball chasing — it causes slipping and long-term back injuries over time (Dr. Dobias)."
                ),
                (
                    "Dental Care", "medium", 5, "19:00", "daily",
                    "Most pets show signs of dental disease by age 3, making daily brushing essential (Gardens Animal Hospital). "
                    "Use pet-safe toothpaste and aim for at least 2–3 sessions per week if daily isn't possible (NaturVet)."
                ),
                (
                    "Groom", "low", 15, "19:30", "weekly",
                    groom_note
                ),
            ]
        elif species == "cat":
            age_note = "kitten" if age < 1 else ("senior" if age >= 7 else "adult")
            raw_tasks = [
                (
                    "Feed", "high", 5, "08:00", "daily",
                    feed_note + " " +
                    f"{'Kittens can be fed free-choice until 1 year old since they need 2–3x the energy of adult cats (ASPCA).' if age_note == 'kitten' else 'Senior cats (7+) should transition to a senior diet and be monitored for weight changes (ASPCA).' if age_note == 'senior' else '60% of cats in the U.S. are overweight — measure portions carefully and limit treats to 5% of daily intake (NaturVet).'}"
                ),
                (
                    "Litter Box", "high", 5, "08:30", "daily",
                    "Scoop the litter box at least once daily — cats avoid dirty boxes which can cause stress and health issues (ASPCA). "
                    "Do a full litter change and box wash at least weekly to prevent bacteria buildup (ASPCA, Mission Vet)."
                ),
                (
                    "Morning Play", "medium", max(10, exercise_duration // 3), "10:00", "daily",
                    exercise_note + " "
                    "Use wand toys that mimic prey movement — always end laser pointer play with a physical toy the cat can 'catch' (American Humane)."
                ),
                (
                    "Evening Play", "medium", max(10, exercise_duration // 3), "17:00", "daily",
                    "A second play session in the evening mirrors a cat's natural hunting pattern of dawn and dusk activity (American Humane). "
                    "Indoor cats need more enrichment than outdoor cats — rotating toys and puzzle feeders prevent boredom (ASPCA)."
                ),
                (
                    "Dental Care", "medium", 5, "19:00", "daily",
                    "Most cats show signs of dental disease by age 3, but cats often hide pain making prevention critical (Gardens Animal Hospital, MHA). "
                    "Brush with pet-safe toothpaste at least 2–3 times per week, or provide vet-approved dental chews (NaturVet, OVRS)."
                ),
                (
                    "Groom", "low", 10, "19:30", "daily",
                    groom_note
                ),
            ]
        else:
            # Any other species — fully driven by You.com search results for that species/breed
            raw_tasks = [
                (
                    "Feed", "high", 10, "08:00", "daily",
                    feed_note + " Always provide fresh, clean water and measure portions to prevent obesity (OVRS)."
                ),
                (
                    "Playtime", "medium", max(15, exercise_duration // 2), "10:00", "daily",
                    exercise_note + " "
                    "Daily play and enrichment reduces anxiety, destructive behavior, and obesity in pets (FPC Vets)."
                ),
                (
                    "Exercise", "medium", exercise_duration, "14:00", "daily",
                    exercise_note + " "
                    "Consult your vet for exercise recommendations specific to your pet's species, age, and breed (Mokena Animal Clinic)."
                ),
                (
                    "Groom", "low", 10, "19:00", "weekly",
                    groom_note
                ),
            ]

        tasks = []
        for name, priority, duration, start_time, recurrence, reasoning in raw_tasks:
            task = Task(name, priority, duration, start_time, recurrence)
            task.reasoning = reasoning
            tasks.append(task)

        return tasks
    
    def explain_recommendations(self, tasks: List[Task]) -> str:
        """
        Generate explanation of why tasks were recommended.
        
        Args:
            tasks: List of recommended tasks
            
        Returns:
            Human-readable explanation
        """
        explanations = []
        for task in tasks:
            if hasattr(task, 'reasoning') and task.reasoning:
                explanations.append(f"• {task.name}: {task.reasoning}")
            else:
                explanations.append(f"• {task.name} ({task.priority} priority, {task.duration}m)")
        
        return "Task Recommendations Based on Pet Care Guidelines:\n" + "\n".join(explanations)
