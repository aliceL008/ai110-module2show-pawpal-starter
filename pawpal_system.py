from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    name: str
    priority: str
    duration: int

    def set_duration(self, duration: int) -> None:
        """Update task duration in minutes."""
        self.duration = duration

    def set_priority(self, level: str) -> None:
        """Update task priority (e.g., low/medium/high)."""
        self.priority = level


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a Task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, name: str) -> None:
        """Remove a task by name."""
        self.tasks = [task for task in self.tasks if task.name != name]

    def view_tasks(self) -> List[Task]:
        """Return the task list for this pet."""
        return list(self.tasks)


class User:
    def __init__(self, name: str):
        self.name = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a Pet to the user's pet list."""
        self.pets.append(pet)

    def remove_pet(self, name: str) -> None:
        """Remove a pet by name."""
        self.pets = [pet for pet in self.pets if pet.name != name]

    def view_pets(self) -> List[Pet]:
        """Return the user's pets."""
        return list(self.pets)


class Scheduler:
    def __init__(self, tasks: List[Task], time_available: int):
        self.tasks = tasks
        self.time_available = time_available

    def sort_by_priority(self) -> List[Task]:
        """Return tasks sorted by priority (high -> low)."""
        priority_order = {'high': 1, 'medium': 2, 'low': 3}
        return sorted(self.tasks, key=lambda t: priority_order.get(t.priority.lower(), 99))

    def fit_times(self) -> List[Task]:
        """Select tasks that fit in the available time."""
        result = []
        remaining = self.time_available
        for task in self.sort_by_priority():
            if task.duration <= remaining:
                result.append(task)
                remaining -= task.duration
        return result

    def make_schedule(self) -> List[Task]:
        """Build the schedule by fitting highest priority tasks into available time."""
        return self.fit_times()

    def explain_fit(self) -> str:
        """Explain why tasks were selected to fill the schedule."""
        scheduled = self.make_schedule()
        if not scheduled:
            return "No tasks could be scheduled in the available time."

        lines = [f"Scheduled {task.name} ({task.priority}, {task.duration}m)" for task in scheduled]
        used = sum(task.duration for task in scheduled)
        return (
            "Selected tasks in priority order until time ran out:\n" +
            "\n".join(lines) +
            f"\nTotal used: {used}m / {self.time_available}m"
        )

