from pawpal_system import User, Pet, Task, Scheduler

def main():
    # Create owner
    owner = User("Alice")

    # Create pets
    pet1 = Pet("Fluffy", "Cat", 3)
    pet2 = Pet("Buddy", "Dog", 5)

    # Add tasks to pets — task1 and task3 intentionally overlap at 08:00
    task1 = Task("Feed",  "high",   10, start_time="08:00", recurrence="daily")
    task2 = Task("Play",  "medium", 20, start_time="10:00", recurrence="daily")
    task3 = Task("Groom", "low",    15, start_time="08:05", recurrence="weekly")  # overlaps Feed

    pet1.add_task(task1)
    pet1.add_task(task2)
    pet2.add_task(task3)
  


    # Add pets to owner
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    # Create scheduler with 45 minutes available
    scheduler = Scheduler(owner, 45)

    # Get schedule
    schedule = scheduler.make_schedule()
    explanation = scheduler.explain_fit()

    # Print Today's Schedule
    print("Today's Schedule")
    print("=" * 20)
    for task in schedule:
        print(f"- {task.name} ({task.priority} priority, {task.duration} minutes)")
    print("\nExplanation:")
    print(explanation)

    # Conflict detection
    print("\n--- Conflict Check ---")
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            print(warning)
    else:
        print("No scheduling conflicts found.")

    # Test filter_tasks: all incomplete tasks
    print("\n--- Filter: incomplete tasks (all pets) ---")
    for task in owner.filter_tasks(status="incomplete"):
        print(f"- {task.name} [{task.status}]")

    # Test filter_tasks: tasks for Fluffy only
    print("\n--- Filter: Fluffy's tasks ---")
    for task in owner.filter_tasks(pet_name="Fluffy"):
        print(f"- {task.name} ({task.priority})")

    # Test sort by duration inside fit_times (schedule already sorted by priority)
    print("\n--- Tasks sorted by duration (shortest first) ---")
    all_tasks = owner.get_all_tasks()
    for task in sorted(all_tasks, key=lambda t: t.duration):
        print(f"- {task.name}: {task.duration}m ({task.priority})")

if __name__ == "__main__":
    main()
