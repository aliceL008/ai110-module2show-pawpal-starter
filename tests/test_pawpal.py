from pawpal_system import Task, Pet


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
