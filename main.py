
from dotenv import load_dotenv
load_dotenv()
from pawpal_system import User, Pet, Scheduler
from rag.rag_recommender import RAGTaskRecommender

def main():
    """
    Main demo: Uses RAG to recommend tasks, then schedules them.
    Shows how knowledge-based recommendations improve pet care planning.
    """
    print("=" * 60)
    print("PawPal+ with RAG - Pet Care Planning System")
    print("=" * 60)
    
    # Create owner
    owner = User("Alice")
    
    # Create pets
    dog = Pet("Buddy", "Dog", 5)
    cat = Pet("Whiskers", "Cat", 3)
    
    owner.add_pet(dog)
    owner.add_pet(cat)
    
    # Initialize RAG recommender
    print("\n📚 Initializing RAG Task Recommender...")
    recommender = RAGTaskRecommender()
    print("✓ RAG system ready\n")
    
    # === RETRIEVE KNOWLEDGE FOR DOG ===
    print("-" * 60)
    print("🐕 DOG: Buddy (5 years old)")
    print("-" * 60)
    
    print("\n🔍 Retrieving pet care guidelines from knowledge base...")
    dog_feeding_context = recommender._retrieve_context(dog, "feeding")
    dog_exercise_context = recommender._retrieve_context(dog, "exercise")
    
    print(f"✓ Retrieved {len(dog_feeding_context)} chars of feeding guidelines")
    print(f"✓ Retrieved {len(dog_exercise_context)} chars of exercise guidelines")
    
    print("\n💡 Generating task recommendations based on veterinary guidelines...")
    dog_tasks = recommender.recommend_tasks(dog, owner_constraints="2 hours available daily")
    
    for task in dog_tasks:
        print(f"  ✓ {task.name}: {task.duration}m ({task.priority}), {task.recurrence}")
    
    # Add recommended tasks to dog
    for task in dog_tasks:
        dog.add_task(task)
    
    # === RETRIEVE KNOWLEDGE FOR CAT ===
    print("\n" + "-" * 60)
    print("🐱 CAT: Whiskers (3 years old)")
    print("-" * 60)
    
    print("\n🔍 Retrieving pet care guidelines from knowledge base...")
    cat_feeding_context = recommender._retrieve_context(cat, "feeding")
    cat_play_context = recommender._retrieve_context(cat, "play")
    
    print(f"✓ Retrieved {len(cat_feeding_context)} chars of feeding guidelines")
    print(f"✓ Retrieved {len(cat_play_context)} chars of play guidelines")
    
    print("\n💡 Generating task recommendations based on veterinary guidelines...")
    cat_tasks = recommender.recommend_tasks(cat, owner_constraints="1 hour available daily")
    
    for task in cat_tasks:
        print(f"  ✓ {task.name}: {task.duration}m ({task.priority}), {task.recurrence}")
    
    # Add recommended tasks to cat
    for task in cat_tasks:
        cat.add_task(task)
    
    # === SCHEDULE TASKS ===
    print("\n" + "=" * 60)
    print("📅 SCHEDULING - Fitting tasks into available time")
    print("=" * 60)
    
    available_time = 120  # 2 hours
    scheduler = Scheduler(owner, available_time)
    
    print(f"\n⏰ Available time: {available_time} minutes")
    print(f"📋 Total tasks available: {len(scheduler.tasks)}")
    
    schedule = scheduler.make_schedule()
    explanation = scheduler.explain_fit()
    
    print("\n📋 Today's Prioritized Schedule:")
    print("-" * 40)
    for task in schedule:
        print(f"  {task.start_time} | {task.name:15} | {task.duration:3}m | {task.priority}")
    
    print("\n📖 Scheduling Explanation:")
    print("-" * 40)
    print(explanation)
    
    # === CONFLICT DETECTION ===
    print("\n" + "-" * 60)
    print("⚠️  CONFLICT CHECK")
    print("-" * 60)
    
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        print("\n⚠️  Detected scheduling conflicts:")
        for warning in conflicts:
            print(f"  • {warning}")
    else:
        print("\n✓ No scheduling conflicts found.")
    
    # === HUMAN VALIDATION ===
    print("\n" + "=" * 60)
    print("✅ HUMAN VALIDATION & FEEDBACK")
    print("=" * 60)
    
    print("\n📋 Recommendation Explanations (for owner review):")
    print("-" * 40)
    
    print("\nDog Recommendations:")
    dog_explanation = recommender.explain_recommendations(dog_tasks)
    print(dog_explanation)
    
    print("\nCat Recommendations:")
    cat_explanation = recommender.explain_recommendations(cat_tasks)
    print(cat_explanation)
    
    # === FILTER & ANALYZE ===
    print("\n" + "=" * 60)
    print("🔎 TASK ANALYSIS")
    print("=" * 60)
    
    print("\n📊 Task Summary by Priority:")
    all_tasks = owner.get_all_tasks()
    for priority in ["high", "medium", "low"]:
        count = len([t for t in all_tasks if t.priority == priority])
        total_time = sum(t.duration for t in all_tasks if t.priority == priority)
        print(f"  {priority.upper():8}: {count} tasks, {total_time} total minutes")
    
    print("\n🐾 Tasks by Pet:")
    for pet in owner.view_pets():
        tasks = pet.view_tasks()
        total_time = sum(t.duration for t in tasks)
        print(f"  {pet.name:12}: {len(tasks)} tasks, {total_time} total minutes")
    
    print("\n" + "=" * 60)
    print("✨ Demo Complete!")
    print("=" * 60)
    print("\nKey Features Demonstrated:")
    print("  ✓ RAG knowledge retrieval based on pet species & age")
    print("  ✓ AI task recommendations grounded in veterinary guidelines")
    print("  ✓ Intelligent scheduling with priority & time constraints")
    print("  ✓ Conflict detection between overlapping tasks")
    print("  ✓ Human-readable explanations for validation")
    print("  ✓ Filtering and analysis of task sets")


if __name__ == "__main__":
    main()
