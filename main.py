from pawpal_system import User, Pet, Task, Scheduler

def main():
    # Create owner
    owner = User("Alice")

    # Create pets
    pet1 = Pet("Fluffy", "Cat", 3)
    pet2 = Pet("Buddy", "Dog", 5)

    # Add tasks to pets
    task1 = Task("Feed", "high", 10)
    task2 = Task("Play", "medium", 20)
    task3 = Task("Groom", "low", 15)

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

if __name__ == "__main__":
    main()
