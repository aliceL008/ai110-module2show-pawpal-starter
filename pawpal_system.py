from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List, Optional


@dataclass
class Task:
    name: str
    priority: str
    duration: int
    start_time: str = "00:00"
    status: str = "incomplete"
    recurrence: Optional[str] = None  # "daily", "weekly", or None
    due_date: Optional[date] = None   # calculated on next_occurrence()

    def mark_complete(self) -> None:
        """Mark this task as complete."""
        self.status = "complete"

    def next_occurrence(self) -> Optional["Task"]:
        """
        Return a fresh incomplete copy of this task for its next occurrence.

        Uses timedelta to calculate the due date:
          - "daily"  → today + 1 day
          - "weekly" → today + 7 days
          - None or any other value → returns None (one-time task, no renewal)
        """
        if self.recurrence == "daily":
            next_due = date.today() + timedelta(days=1)
        elif self.recurrence == "weekly":
            next_due = date.today() + timedelta(days=7)
        else:
            return None
        return Task(
            name=self.name,
            priority=self.priority,
            duration=self.duration,
            start_time=self.start_time,
            status="incomplete",
            recurrence=self.recurrence,
            due_date=next_due,
        )

    def set_duration(self, duration: int) -> None:
        """Update task duration in minutes. Must be positive."""
        if duration <= 0:
            raise ValueError("Duration must be positive.")
        self.duration = duration

    def set_priority(self, level: str) -> None:
        """Update task priority (e.g., low/medium/high)."""
        valid_priorities = {'low', 'medium', 'high'}
        if level.lower() not in valid_priorities:
            raise ValueError(f"Priority must be one of {valid_priorities}.")
        self.priority = level.lower()


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
        """Initialize a User with a name and an empty pet list."""
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

    def get_all_tasks(self) -> List[Task]:
        """Aggregate all tasks from all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def filter_tasks(self, status: str = None, pet_name: str = None) -> List[Task]:
        """
        Return tasks filtered by completion status, pet name, or both.

        Args:
            status:   "complete" or "incomplete". Omit to include all statuses.
            pet_name: Name of a specific pet. Omit to include tasks from all pets.

        Both filters are case-insensitive. Skips a pet entirely if pet_name
        does not match, avoiding unnecessary task iteration.
        """
        results = []
        for pet in self.pets:
            if pet_name and pet.name.lower() != pet_name.lower():
                continue
            for task in pet.tasks:
                if status and task.status.lower() != status.lower():
                    continue
                results.append(task)
        return results


class Scheduler:
    def __init__(self, user: User, time_available: int):
        """Initialize a Scheduler with a user and total available time in minutes."""
        self.user = user
        self.tasks = user.get_all_tasks()
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
        return sorted(result, key=lambda t: (int(t.start_time[:2]), int(t.start_time[3:])))

    def make_schedule(self) -> List[Task]:
        """Build the schedule by fitting highest priority tasks into available time."""
        return self.fit_times()

    def _to_minutes(self, time_str: str) -> int:
        """
        Convert a 'HH:MM' time string to total minutes since midnight.

        Used internally by detect_conflicts() to compare task start/end times
        as plain integers instead of strings.
        Example: "08:30" → 510
        """
        hours, mins = time_str.split(":")
        return int(hours) * 60 + int(mins)

    def detect_conflicts(self) -> List[str]:
        """
        Check all scheduled tasks for time overlaps and return warning messages.

        Uses a pairwise comparison strategy: for every pair of tasks (a, b),
        checks if their time windows intersect using the condition:
            a_start < b_end  and  b_start < a_end

        Returns a list of warning strings describing each conflict found.
        Returns an empty list if no conflicts exist.
        Never raises an exception — warnings are informational only and
        do not remove tasks from the schedule.
        """
        scheduled = self.make_schedule()
        warnings = []

        for i in range(len(scheduled)):
            for j in range(i + 1, len(scheduled)):
                a = scheduled[i]
                b = scheduled[j]
                a_start = self._to_minutes(a.start_time)
                a_end   = a_start + a.duration
                b_start = self._to_minutes(b.start_time)
                b_end   = b_start + b.duration

                if a_start < b_end and b_start < a_end:
                    warnings.append(
                        f"WARNING: '{a.name}' ({a.start_time}, {a.duration}m) "
                        f"overlaps with '{b.name}' ({b.start_time}, {b.duration}m)"
                    )

        return warnings

    def check_and_renew(self) -> List[Task]:
        """
        Auto-generate the next plan once all scheduled tasks are marked complete.

        Iterates over every pet's tasks and calls next_occurrence() on each.
        Recurring tasks ("daily" or "weekly") get a fresh copy with a new
        due_date added back to the pet. The scheduler's task list is then
        refreshed and a new schedule is returned.

        Returns:
            A new List[Task] schedule if all tasks were complete and renewals exist.
            An empty list if any task is still incomplete, or no tasks recur.
        """
        scheduled = self.make_schedule()
        if any(t.status != "complete" for t in scheduled):
            return []

        renewed = []
        for pet in self.user.pets:
            for task in list(pet.tasks):
                next_task = task.next_occurrence()
                if next_task:
                    pet.add_task(next_task)
                    renewed.append(next_task)

        if renewed:
            self.tasks = self.user.get_all_tasks()
            print("\nAll tasks complete! New plan generated for next occurrence:")
            for t in renewed:
                print(f"  + {t.name} ({t.recurrence}, {t.priority}, {t.duration}m)")
            return self.make_schedule()

        print("\nAll tasks complete! No recurring tasks to renew.")
        return []

    def explain_fit(self) -> str:
        """Explain why tasks were selected to fill the schedule."""
        scheduled = self.make_schedule()
        all_sorted = self.sort_by_priority()
        skipped = [task for task in all_sorted if task not in scheduled]
        
        if not scheduled:
            return "No tasks could be scheduled in the available time."

        lines = [f"Scheduled {task.name} ({task.priority}, {task.duration}m)" for task in scheduled]
        used = sum(task.duration for task in scheduled)
        explanation = (
            "Selected tasks in priority order until time ran out:\n" +
            "\n".join(lines) +
            f"\nTotal used: {used}m / {self.time_available}m"
        )
        if skipped:
            skipped_lines = [f"Skipped {task.name} ({task.priority}, {task.duration}m)" for task in skipped]
            explanation += "\n\nSkipped due to time constraints:\n" + "\n".join(skipped_lines)
        return explanation

