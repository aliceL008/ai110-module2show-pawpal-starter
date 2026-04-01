from datetime import date, timedelta
from pawpal_system import Task, Pet, User, Scheduler


def test_task_default_status_is_incomplete():
    task = Task(name="Feed Buddy", priority="high", duration=10)
    assert task.status == "incomplete"


def test_mark_complete_changes_status():
    task = Task(name="Feed Buddy", priority="high", duration=10)
    task.mark_complete()
    assert task.status == "complete"


def test_mark_complete_is_idempotent():
    task = Task(name="Walk Rex", priority="medium", duration=30)
    task.mark_complete()
    task.mark_complete()
    assert task.status == "complete"


def test_mark_complete_does_not_affect_other_fields():
    task = Task(name="Vet Visit", priority="high", duration=60)
    task.mark_complete()
    assert task.name == "Vet Visit"
    assert task.priority == "high"
    assert task.duration == 60


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Buddy", species="dog", age=3)
    task = Task(name="Feed Buddy", priority="high", duration=10)
    assert len(pet.view_tasks()) == 0
    pet.add_task(task)
    assert len(pet.view_tasks()) == 1


def test_mark_complete_on_separate_tasks_are_independent():
    task1 = Task(name="Feed Buddy", priority="high", duration=10)
    task2 = Task(name="Walk Rex", priority="low", duration=20)
    task1.mark_complete()
    assert task1.status == "complete"
    assert task2.status == "incomplete"


# --- Sorting Correctness ---

def test_fit_times_returns_tasks_in_chronological_order():
    """Tasks in the schedule are sorted by start_time, earliest first."""
    pet = Pet(name="Buddy", species="dog", age=3)
    pet.add_task(Task(name="Evening Walk",  priority="high", duration=20, start_time="18:00"))
    pet.add_task(Task(name="Morning Feed",  priority="high", duration=10, start_time="07:00"))
    pet.add_task(Task(name="Midday Meds",   priority="high", duration=5,  start_time="12:00"))

    user = User(name="Alice")
    user.add_pet(pet)
    scheduler = Scheduler(user=user, time_available=120)

    schedule = scheduler.make_schedule()
    start_times = [t.start_time for t in schedule]
    assert start_times == sorted(start_times), "Tasks should be in chronological order"


def test_fit_times_with_single_task_is_still_ordered():
    """A single-task schedule should not crash and be returned as-is."""
    pet = Pet(name="Rex", species="dog", age=2)
    pet.add_task(Task(name="Only Task", priority="medium", duration=15, start_time="09:00"))

    user = User(name="Alice")
    user.add_pet(pet)
    scheduler = Scheduler(user=user, time_available=60)

    schedule = scheduler.make_schedule()
    assert len(schedule) == 1
    assert schedule[0].name == "Only Task"


# --- Recurrence Logic ---

def test_daily_task_next_occurrence_is_tomorrow():
    """next_occurrence() on a daily task produces a task due tomorrow."""
    task = Task(name="Feed Buddy", priority="high", duration=10, recurrence="daily")
    next_task = task.next_occurrence()

    assert next_task is not None
    assert next_task.due_date == date.today() + timedelta(days=1)
    assert next_task.status == "incomplete"
    assert next_task.recurrence == "daily"


def test_weekly_task_next_occurrence_is_seven_days_out():
    """next_occurrence() on a weekly task produces a task due in 7 days."""
    task = Task(name="Vet Check", priority="high", duration=60, recurrence="weekly")
    next_task = task.next_occurrence()

    assert next_task is not None
    assert next_task.due_date == date.today() + timedelta(days=7)


def test_non_recurring_task_next_occurrence_returns_none():
    """A one-time task should return None from next_occurrence()."""
    task = Task(name="One-time Bath", priority="low", duration=30, recurrence=None)
    assert task.next_occurrence() is None


def test_check_and_renew_generates_next_occurrence_after_all_complete():
    """Marking all tasks complete and calling check_and_renew adds next-day copies."""
    pet = Pet(name="Buddy", species="dog", age=3)
    daily_task = Task(name="Morning Feed", priority="high", duration=10,
                      start_time="07:00", recurrence="daily")
    pet.add_task(daily_task)

    user = User(name="Alice")
    user.add_pet(pet)
    scheduler = Scheduler(user=user, time_available=60)

    # Complete all scheduled tasks
    for task in scheduler.make_schedule():
        task.mark_complete()

    new_schedule = scheduler.check_and_renew()

    assert len(new_schedule) >= 1
    # The schedule contains both the old completed task and the new renewed copy.
    # Find the renewed (incomplete) one explicitly.
    renewed = next((t for t in new_schedule if t.status == "incomplete"), None)
    assert renewed is not None, "Expected a renewed incomplete task in the new schedule"
    assert renewed.due_date == date.today() + timedelta(days=1)


def test_check_and_renew_does_nothing_if_tasks_incomplete():
    """check_and_renew returns [] when any task is still incomplete."""
    pet = Pet(name="Buddy", species="dog", age=3)
    pet.add_task(Task(name="Feed", priority="high", duration=10,
                      start_time="08:00", recurrence="daily"))

    user = User(name="Alice")
    user.add_pet(pet)
    scheduler = Scheduler(user=user, time_available=60)

    result = scheduler.check_and_renew()
    assert result == []


# --- Conflict Detection ---

def test_detect_conflicts_flags_overlapping_tasks():
    """Two tasks whose time windows overlap should produce a conflict warning."""
    pet = Pet(name="Buddy", species="dog", age=3)
    # Task A: 08:00 for 30 min → ends 08:30
    # Task B: 08:15 for 30 min → starts before A ends → overlap
    pet.add_task(Task(name="Morning Walk", priority="high", duration=30, start_time="08:00"))
    pet.add_task(Task(name="Morning Feed", priority="high", duration=30, start_time="08:15"))

    user = User(name="Alice")
    user.add_pet(pet)
    scheduler = Scheduler(user=user, time_available=120)

    warnings = scheduler.detect_conflicts()
    assert len(warnings) >= 1
    assert any("Morning Walk" in w and "Morning Feed" in w for w in warnings)


def test_detect_conflicts_same_start_time_flagged():
    """Two tasks starting at exactly the same time must be flagged."""
    pet = Pet(name="Rex", species="dog", age=2)
    pet.add_task(Task(name="Task A", priority="high", duration=15, start_time="09:00"))
    pet.add_task(Task(name="Task B", priority="high", duration=15, start_time="09:00"))

    user = User(name="Alice")
    user.add_pet(pet)
    scheduler = Scheduler(user=user, time_available=120)

    warnings = scheduler.detect_conflicts()
    assert len(warnings) >= 1


def test_detect_conflicts_no_warning_for_sequential_tasks():
    """Tasks that end exactly when the next begins should NOT conflict."""
    pet = Pet(name="Buddy", species="dog", age=3)
    # Task A: 08:00 for 30 min → ends 08:30
    # Task B: 08:30 for 30 min → starts exactly when A ends → no overlap
    pet.add_task(Task(name="Walk",  priority="high", duration=30, start_time="08:00"))
    pet.add_task(Task(name="Feed",  priority="high", duration=30, start_time="08:30"))

    user = User(name="Alice")
    user.add_pet(pet)
    scheduler = Scheduler(user=user, time_available=120)

    warnings = scheduler.detect_conflicts()
    assert warnings == []


# --- Priority Sorting ---

def test_sort_by_priority_orders_high_before_medium_before_low():
    """sort_by_priority returns tasks in high → medium → low order."""
    pet = Pet(name="Buddy", species="dog", age=3)
    pet.add_task(Task(name="Low Task",    priority="low",    duration=10, start_time="10:00"))
    pet.add_task(Task(name="Medium Task", priority="medium", duration=10, start_time="09:00"))
    pet.add_task(Task(name="High Task",   priority="high",   duration=10, start_time="08:00"))

    user = User(name="Alice")
    user.add_pet(pet)
    scheduler = Scheduler(user=user, time_available=120)

    sorted_tasks = scheduler.sort_by_priority()
    priorities = [t.priority for t in sorted_tasks]
    assert priorities == ["high", "medium", "low"]


# --- Time Budget ---

def test_fit_times_skips_task_that_exceeds_available_time():
    """A task too long to fit in remaining time should be excluded from the schedule."""
    pet = Pet(name="Buddy", species="dog", age=3)
    pet.add_task(Task(name="Short Task", priority="high", duration=20, start_time="08:00"))
    pet.add_task(Task(name="Long Task",  priority="high", duration=90, start_time="09:00"))

    user = User(name="Alice")
    user.add_pet(pet)
    scheduler = Scheduler(user=user, time_available=30)  # only 30 min available

    schedule = scheduler.make_schedule()
    names = [t.name for t in schedule]
    assert "Short Task" in names
    assert "Long Task" not in names


def test_fit_times_respects_cumulative_time_budget():
    """Tasks are skipped once cumulative duration exceeds time_available."""
    pet = Pet(name="Rex", species="dog", age=2)
    pet.add_task(Task(name="Task A", priority="high",   duration=30, start_time="08:00"))
    pet.add_task(Task(name="Task B", priority="medium", duration=30, start_time="09:00"))
    pet.add_task(Task(name="Task C", priority="low",    duration=30, start_time="10:00"))

    user = User(name="Alice")
    user.add_pet(pet)
    scheduler = Scheduler(user=user, time_available=50)  # fits A (30) but not B (30 more)

    schedule = scheduler.make_schedule()
    names = [t.name for t in schedule]
    assert "Task A" in names
    assert "Task B" not in names
    assert "Task C" not in names


# --- Pet and User Mutation ---

def test_remove_task_reduces_pet_task_count():
    """remove_task should delete the named task from the pet's list."""
    pet = Pet(name="Buddy", species="dog", age=3)
    pet.add_task(Task(name="Feed", priority="high", duration=10))
    pet.add_task(Task(name="Walk", priority="low",  duration=20))
    pet.remove_task("Feed")
    names = [t.name for t in pet.view_tasks()]
    assert "Feed" not in names
    assert "Walk" in names


def test_remove_pet_reduces_user_pet_count():
    """remove_pet should delete the named pet from the user's list."""
    user = User(name="Alice")
    user.add_pet(Pet(name="Buddy", species="dog", age=3))
    user.add_pet(Pet(name="Whiskers", species="cat", age=2))
    user.remove_pet("Buddy")
    names = [p.name for p in user.view_pets()]
    assert "Buddy" not in names
    assert "Whiskers" in names


# --- filter_tasks ---

def test_filter_tasks_by_status_returns_only_matching():
    """filter_tasks(status='complete') returns only completed tasks."""
    pet = Pet(name="Buddy", species="dog", age=3)
    done = Task(name="Walk", priority="high", duration=20)
    done.mark_complete()
    pet.add_task(done)
    pet.add_task(Task(name="Feed", priority="high", duration=10))

    user = User(name="Alice")
    user.add_pet(pet)

    results = user.filter_tasks(status="complete")
    assert all(t.status == "complete" for t in results)
    assert len(results) == 1


def test_filter_tasks_by_pet_name_excludes_other_pets():
    """filter_tasks(pet_name=...) only returns tasks from that pet."""
    pet1 = Pet(name="Buddy", species="dog", age=3)
    pet1.add_task(Task(name="Walk Buddy", priority="high", duration=20))
    pet2 = Pet(name="Whiskers", species="cat", age=2)
    pet2.add_task(Task(name="Feed Whiskers", priority="low", duration=5))

    user = User(name="Alice")
    user.add_pet(pet1)
    user.add_pet(pet2)

    results = user.filter_tasks(pet_name="Buddy")
    assert all(t.name == "Walk Buddy" for t in results)
    assert len(results) == 1


def test_filter_tasks_by_status_and_pet_name():
    """filter_tasks with both filters applied returns the intersection."""
    pet = Pet(name="Buddy", species="dog", age=3)
    done = Task(name="Walk", priority="high", duration=20)
    done.mark_complete()
    pet.add_task(done)
    pet.add_task(Task(name="Feed", priority="high", duration=10))

    user = User(name="Alice")
    user.add_pet(pet)

    results = user.filter_tasks(status="complete", pet_name="Buddy")
    assert len(results) == 1
    assert results[0].name == "Walk"


# --- Validation ---

def test_set_duration_raises_on_zero():
    """set_duration(0) should raise ValueError."""
    task = Task(name="Walk", priority="high", duration=10)
    try:
        task.set_duration(0)
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_set_duration_raises_on_negative():
    """set_duration with a negative value should raise ValueError."""
    task = Task(name="Walk", priority="high", duration=10)
    try:
        task.set_duration(-5)
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_set_priority_raises_on_invalid_value():
    """set_priority with an unrecognized level should raise ValueError."""
    task = Task(name="Walk", priority="high", duration=10)
    try:
        task.set_priority("urgent")
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_set_priority_accepts_valid_values():
    """set_priority should accept low, medium, and high without raising."""
    task = Task(name="Walk", priority="high", duration=10)
    task.set_priority("low")
    assert task.priority == "low"
    task.set_priority("medium")
    assert task.priority == "medium"
    task.set_priority("high")
    assert task.priority == "high"


# --- explain_fit ---

def test_explain_fit_mentions_scheduled_tasks():
    """explain_fit output should reference tasks that were scheduled."""
    pet = Pet(name="Buddy", species="dog", age=3)
    pet.add_task(Task(name="Morning Walk", priority="high", duration=20, start_time="08:00"))

    user = User(name="Alice")
    user.add_pet(pet)
    scheduler = Scheduler(user=user, time_available=60)

    explanation = scheduler.explain_fit()
    assert "Morning Walk" in explanation


def test_explain_fit_when_nothing_fits():
    """explain_fit returns a sensible message when no tasks can be scheduled."""
    pet = Pet(name="Buddy", species="dog", age=3)
    pet.add_task(Task(name="Long Task", priority="high", duration=120, start_time="08:00"))

    user = User(name="Alice")
    user.add_pet(pet)
    scheduler = Scheduler(user=user, time_available=10)  # too short for any task

    explanation = scheduler.explain_fit()
    assert "No tasks" in explanation


def test_explain_fit_mentions_skipped_tasks():
    """explain_fit should note tasks that were skipped due to time constraints."""
    pet = Pet(name="Buddy", species="dog", age=3)
    pet.add_task(Task(name="Short Task", priority="high",   duration=10, start_time="08:00"))
    pet.add_task(Task(name="Long Task",  priority="medium", duration=90, start_time="09:00"))

    user = User(name="Alice")
    user.add_pet(pet)
    scheduler = Scheduler(user=user, time_available=20)

    explanation = scheduler.explain_fit()
    assert "Long Task" in explanation
    assert "Skipped" in explanation


# --- Mixed recurrence in check_and_renew ---

def test_check_and_renew_only_renews_recurring_tasks():
    """One-time tasks should not reappear after check_and_renew."""
    pet = Pet(name="Buddy", species="dog", age=3)
    pet.add_task(Task(name="Daily Feed", priority="high", duration=10,
                      start_time="07:00", recurrence="daily"))
    pet.add_task(Task(name="One-time Bath", priority="low", duration=30,
                      start_time="10:00", recurrence=None))

    user = User(name="Alice")
    user.add_pet(pet)
    scheduler = Scheduler(user=user, time_available=120)

    for task in scheduler.make_schedule():
        task.mark_complete()

    new_schedule = scheduler.check_and_renew()

    renewed_names = [t.name for t in new_schedule if t.status == "incomplete"]
    assert "Daily Feed" in renewed_names
    assert "One-time Bath" not in renewed_names


# --- Edge Cases ---

def test_pet_with_no_tasks_returns_empty_schedule():
    """A pet with no tasks should produce an empty schedule without crashing."""
    pet = Pet(name="Ghost", species="cat", age=1)
    user = User(name="Alice")
    user.add_pet(pet)
    scheduler = Scheduler(user=user, time_available=60)

    assert scheduler.make_schedule() == []
    assert scheduler.detect_conflicts() == []
    assert scheduler.check_and_renew() == []
