"""
Test suite for RAG Task Recommender — PawPal+
Covers four reliability methods:
  1. Automated unit tests
  2. Confidence scoring
  3. Logging and error handling
  4. Human evaluation output
"""

import logging
import pytest
from pawpal_system import Pet
from rag.rag_recommender import RAGTaskRecommender
from rag.pet_care_kb import PetCareRetriever, VectorStore, PET_CARE_DOCUMENTS

# ── Logging setup ─────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("tests/test_rag.log", mode="w"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)


# ── 1. AUTOMATED UNIT TESTS ───────────────────────────────────────────────────

class TestVectorStore:
    """Knowledge base loads and retrieves correctly."""

    def test_kb_has_documents(self):
        store = VectorStore()
        log.info(f"KB document count: {len(store.documents)}")
        assert len(store.documents) >= 14, "KB should have at least 14 sourced documents"

    def test_all_documents_have_required_fields(self):
        for doc in PET_CARE_DOCUMENTS:
            assert "id" in doc, f"Document missing 'id': {doc}"
            assert "title" in doc, f"Document missing 'title': {doc}"
            assert "content" in doc and doc["content"].strip(), f"Document has empty content: {doc['id']}"
            assert "source" in doc, f"Document missing 'source' citation: {doc['id']}"
            log.info(f"  ✓ {doc['id']} — source: {doc['source'][:60]}")

    def test_dog_exercise_retrieval(self):
        store = VectorStore()
        docs = store.retrieve("dog exercise daily minutes", top_k=2)
        assert len(docs) > 0
        content = " ".join(d["content"] for d in docs).lower()
        assert any(kw in content for kw in ["exercise", "walk", "activity", "minute"])
        log.info("✓ Dog exercise retrieval returned relevant content")

    def test_cat_feeding_retrieval(self):
        store = VectorStore()
        docs = store.retrieve("cat feeding schedule meals", top_k=2)
        assert len(docs) > 0
        content = " ".join(d["content"] for d in docs).lower()
        assert any(kw in content for kw in ["feed", "meal", "food", "diet"])
        log.info("✓ Cat feeding retrieval returned relevant content")

    def test_senior_pet_retrieval(self):
        store = VectorStore()
        docs = store.retrieve("senior dog care older age", top_k=2)
        assert len(docs) > 0
        log.info("✓ Senior pet retrieval returned results")

    def test_dental_care_retrieval(self):
        store = VectorStore()
        docs = store.retrieve("pet dental care teeth brushing", top_k=2)
        assert len(docs) > 0
        content = " ".join(d["content"] for d in docs).lower()
        assert any(kw in content for kw in ["dental", "teeth", "brush", "tooth"])
        log.info("✓ Dental care retrieval returned relevant content")


class TestFallbackRecommendations:
    """Fallback produces valid, reasonable tasks for all species."""

    def setup_method(self):
        self.recommender = RAGTaskRecommender()

    def test_dog_tasks_have_feed_and_exercise(self):
        dog = Pet("Buddy", "dog", 5)
        tasks = self.recommender._fallback_recommendations(dog)
        names = [t.name.lower() for t in tasks]
        assert any("feed" in n for n in names), "Missing feeding task for dog"
        assert any("exercise" in n or "walk" in n or "play" in n for n in names), "Missing activity task for dog"
        log.info(f"✓ Dog tasks: {[t.name for t in tasks]}")

    def test_cat_tasks_have_litter_and_play(self):
        cat = Pet("Whiskers", "cat", 3)
        tasks = self.recommender._fallback_recommendations(cat)
        names = [t.name.lower() for t in tasks]
        assert any("feed" in n for n in names), "Missing feeding task for cat"
        assert any("litter" in n for n in names), "Missing litter box task for cat"
        assert any("play" in n for n in names), "Missing play task for cat"
        log.info(f"✓ Cat tasks: {[t.name for t in tasks]}")

    def test_all_tasks_have_valid_fields(self):
        for species, age in [("dog", 5), ("cat", 3), ("rabbit", 2)]:
            pet = Pet("TestPet", species, age)
            tasks = self.recommender._fallback_recommendations(pet)
            for t in tasks:
                assert t.name and len(t.name) > 0, "Task has empty name"
                assert t.priority in ["high", "medium", "low"], f"Invalid priority: {t.priority}"
                assert 1 <= t.duration <= 120, f"Unreasonable duration: {t.duration}"
                assert ":" in t.start_time, f"Invalid time format: {t.start_time}"
            log.info(f"✓ All {species} task fields valid")

    def test_feeding_is_high_priority(self):
        for species in ["dog", "cat"]:
            pet = Pet("TestPet", species, 3)
            tasks = self.recommender._fallback_recommendations(pet)
            feed_tasks = [t for t in tasks if "feed" in t.name.lower()]
            for t in feed_tasks:
                assert t.priority == "high", f"Feeding should be high priority, got: {t.priority}"
        log.info("✓ Feeding tasks are high priority for all species")

    def test_tasks_have_sourced_reasoning(self):
        dog = Pet("Buddy", "dog", 5)
        tasks = self.recommender._fallback_recommendations(dog)
        tasks_with_reasoning = [t for t in tasks if getattr(t, "reasoning", "")]
        ratio = len(tasks_with_reasoning) / len(tasks)
        log.info(f"Tasks with reasoning: {len(tasks_with_reasoning)}/{len(tasks)} ({ratio:.0%})")
        assert ratio >= 0.5, "At least 50% of tasks should have sourced reasoning"

    def test_puppy_age_adjusts_tasks(self):
        puppy = Pet("Pup", "dog", 0)
        tasks = self.recommender._fallback_recommendations(puppy)
        feed_task = next((t for t in tasks if "feed" in t.name.lower()), None)
        assert feed_task is not None
        assert "puppy" in feed_task.reasoning.lower() or "meal" in feed_task.reasoning.lower()
        log.info("✓ Puppy age produces age-appropriate reasoning")

    def test_senior_age_adjusts_tasks(self):
        senior = Pet("Rex", "dog", 10)
        tasks = self.recommender._fallback_recommendations(senior)
        reasoning_text = " ".join(getattr(t, "reasoning", "") for t in tasks).lower()
        assert "senior" in reasoning_text or "older" in reasoning_text or "gentle" in reasoning_text
        log.info("✓ Senior age produces age-appropriate reasoning")

    def test_total_daily_time_not_excessive(self):
        dog = Pet("Buddy", "dog", 5)
        tasks = self.recommender._fallback_recommendations(dog)
        total = sum(t.duration for t in tasks if t.recurrence == "daily")
        log.info(f"Total daily task time for dog: {total} minutes")
        assert total <= 180, f"Daily time {total}m is excessive (> 3 hours)"


class TestKBRetriever:
    """PetCareRetriever returns relevant context for different queries."""

    def test_retriever_returns_content(self):
        retriever = PetCareRetriever()
        context = retriever.retrieve(pet_species="dog", pet_age=5, query_topic="feeding")
        assert len(context) > 50, "Context too short to be useful"
        log.info(f"✓ Retriever returned {len(context)} chars for dog feeding")

    def test_retriever_content_is_topic_relevant(self):
        retriever = PetCareRetriever()
        context = retriever.retrieve(pet_species="cat", pet_age=3, query_topic="grooming").lower()
        assert any(kw in context for kw in ["groom", "brush", "coat", "fur", "nail"])
        log.info("✓ Grooming context contains relevant keywords")

    def test_retriever_works_for_multiple_topics(self):
        retriever = PetCareRetriever()
        topics = ["feeding", "exercise", "grooming", "training", "dental care", "play"]
        for topic in topics:
            ctx = retriever.retrieve(pet_species="dog", pet_age=4, query_topic=topic)
            assert len(ctx) > 0, f"Empty context for topic: {topic}"
        log.info(f"✓ Retriever works for all {len(topics)} topics")


# ── 2. CONFIDENCE SCORING ─────────────────────────────────────────────────────

class TestConfidenceScoring:
    """AI rates how sure it is in each recommendation set."""

    def setup_method(self):
        self.recommender = RAGTaskRecommender()

    def test_fallback_confidence_is_scored(self):
        dog = Pet("Buddy", "dog", 5)
        tasks = self.recommender._fallback_recommendations(dog)
        scores = self.recommender.score_confidence(tasks, used_ai=False, breed_data_found=False)
        assert "overall" in scores
        assert 0.0 <= scores["overall"] <= 1.0
        log.info(f"Fallback confidence scores: {scores}")

    def test_ai_mode_scores_higher_than_fallback(self):
        dog = Pet("Buddy", "dog", 5)
        tasks = self.recommender._fallback_recommendations(dog)
        fallback_score = self.recommender.score_confidence(tasks, used_ai=False, breed_data_found=False)
        ai_score = self.recommender.score_confidence(tasks, used_ai=True, breed_data_found=True)
        assert ai_score["overall"] > fallback_score["overall"], \
            "AI-generated recommendations should score higher confidence than fallback"
        log.info(f"Fallback overall: {fallback_score['overall']} | AI overall: {ai_score['overall']}")

    def test_breed_data_improves_confidence(self):
        dog = Pet("Buddy", "dog", 5)
        tasks = self.recommender._fallback_recommendations(dog)
        no_breed = self.recommender.score_confidence(tasks, used_ai=False, breed_data_found=False)
        with_breed = self.recommender.score_confidence(tasks, used_ai=False, breed_data_found=True)
        assert with_breed["overall"] >= no_breed["overall"]
        log.info(f"No breed: {no_breed['overall']} | With breed: {with_breed['overall']}")

    def test_tasks_with_reasoning_score_higher(self):
        dog = Pet("Buddy", "dog", 5)
        tasks = self.recommender._fallback_recommendations(dog)
        # Strip reasoning from copies
        from pawpal_system import Task
        bare_tasks = [Task(t.name, t.priority, t.duration, t.start_time, t.recurrence) for t in tasks]
        score_with = self.recommender.score_confidence(tasks, used_ai=False, breed_data_found=False)
        score_bare = self.recommender.score_confidence(bare_tasks, used_ai=False, breed_data_found=False)
        assert score_with["has_reasoning"] > score_bare["has_reasoning"]
        log.info(f"With reasoning: {score_with['has_reasoning']} | Without: {score_bare['has_reasoning']}")

    def test_confidence_threshold_acceptable(self):
        """Fallback confidence should be at least 0.5 to be usable."""
        dog = Pet("Buddy", "dog", 5)
        tasks = self.recommender._fallback_recommendations(dog)
        scores = self.recommender.score_confidence(tasks, used_ai=False, breed_data_found=False)
        assert scores["overall"] >= 0.5, \
            f"Fallback confidence {scores['overall']} is too low to trust"
        log.info(f"✓ Fallback confidence {scores['overall']} meets minimum threshold of 0.5")


# ── 3. LOGGING AND ERROR HANDLING ────────────────────────────────────────────

class TestErrorHandling:
    """System degrades gracefully and logs failures."""

    def test_recommender_works_without_api_key(self):
        """No API key → fallback, not crash."""
        recommender = RAGTaskRecommender(api_key="invalid-key-xyz")
        dog = Pet("Buddy", "dog", 5)
        try:
            tasks = recommender.recommend_tasks(dog)
            assert len(tasks) > 0
            log.info("✓ System handled missing API key gracefully with fallback")
        except Exception as e:
            log.error(f"System crashed on bad API key: {e}")
            pytest.fail(f"Should not crash with bad API key: {e}")

    def test_empty_breed_does_not_crash(self):
        recommender = RAGTaskRecommender()
        dog = Pet("Buddy", "dog", 5)
        dog.breed = ""
        try:
            tasks = recommender._fallback_recommendations(dog)
            assert len(tasks) > 0
            log.info("✓ Empty breed handled without crash")
        except Exception as e:
            log.error(f"Crash on empty breed: {e}")
            pytest.fail(str(e))

    def test_unknown_species_returns_tasks(self):
        recommender = RAGTaskRecommender()
        pet = Pet("Hoppy", "rabbit", 2)
        try:
            tasks = recommender._fallback_recommendations(pet)
            assert len(tasks) > 0
            log.info(f"✓ Unknown species 'rabbit' returned {len(tasks)} tasks")
        except Exception as e:
            log.error(f"Crash on unknown species: {e}")
            pytest.fail(str(e))

    def test_extreme_age_does_not_crash(self):
        recommender = RAGTaskRecommender()
        for age in [0, 1, 20]:
            pet = Pet("OldDog", "dog", age)
            try:
                tasks = recommender._fallback_recommendations(pet)
                assert len(tasks) > 0
                log.info(f"✓ Age {age} handled correctly")
            except Exception as e:
                log.error(f"Crash at age {age}: {e}")
                pytest.fail(str(e))

    def test_duration_extraction_handles_bad_input(self):
        recommender = RAGTaskRecommender()
        assert recommender._extract_duration("", default=30) == 30
        assert recommender._extract_duration("no numbers here", default=45) == 45
        assert recommender._extract_duration("exercise for 60 minutes daily", default=30) == 60
        assert recommender._extract_duration("walk 1 hour per day", default=30) == 60
        log.info("✓ Duration extraction handles edge cases correctly")


# ── 4. HUMAN EVALUATION OUTPUT ───────────────────────────────────────────────

class TestHumanEvaluation:
    """
    Generates readable output for a human reviewer to assess quality.
    Run with: pytest tests/test_rag.py::TestHumanEvaluation -v -s
    """

    def test_print_dog_sample_output(self):
        recommender = RAGTaskRecommender()
        dog = Pet("Buddy", "dog", 5)
        dog.breed = "Golden Retriever"
        tasks = recommender._fallback_recommendations(dog)
        scores = recommender.score_confidence(tasks, used_ai=False, breed_data_found=False)

        print("\n" + "=" * 60)
        print("HUMAN EVALUATION — Dog (Golden Retriever, 5 years)")
        print("=" * 60)
        for t in tasks:
            print(f"\n  [{t.priority.upper()}] {t.name} — {t.start_time} · {t.duration} min")
            print(f"  Reasoning: {getattr(t, 'reasoning', 'N/A')[:120]}...")
        print(f"\n  Confidence scores: {scores}")
        print("=" * 60)
        assert len(tasks) > 0

    def test_print_cat_sample_output(self):
        recommender = RAGTaskRecommender()
        cat = Pet("Luna", "cat", 2)
        cat.breed = "Persian"
        tasks = recommender._fallback_recommendations(cat)
        scores = recommender.score_confidence(tasks, used_ai=False, breed_data_found=False)

        print("\n" + "=" * 60)
        print("HUMAN EVALUATION — Cat (Persian, 2 years)")
        print("=" * 60)
        for t in tasks:
            print(f"\n  [{t.priority.upper()}] {t.name} — {t.start_time} · {t.duration} min")
            print(f"  Reasoning: {getattr(t, 'reasoning', 'N/A')[:120]}...")
        print(f"\n  Confidence scores: {scores}")
        print("=" * 60)
        assert len(tasks) > 0

    def test_print_other_species_output(self):
        recommender = RAGTaskRecommender()
        rabbit = Pet("Thumper", "rabbit", 1)
        rabbit.breed = "Holland Lop"
        tasks = recommender._fallback_recommendations(rabbit)
        scores = recommender.score_confidence(tasks, used_ai=False, breed_data_found=False)

        print("\n" + "=" * 60)
        print("HUMAN EVALUATION — Rabbit (Holland Lop, 1 year)")
        print("=" * 60)
        for t in tasks:
            print(f"\n  [{t.priority.upper()}] {t.name} — {t.start_time} · {t.duration} min")
            print(f"  Reasoning: {getattr(t, 'reasoning', 'N/A')[:120]}...")
        print(f"\n  Confidence scores: {scores}")
        print("=" * 60)
        assert len(tasks) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
