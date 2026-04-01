# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Smarter Scheduling 
PawPal+ was extended with features to make the scheduler more practical and easier to use. Tasks now include a time field so the daily plan can be shown in chronological order while still considering priority. Recurring tasks can be set as daily or weekly, and once all tasks are completed, the scheduler automatically generates the next plan using updated dates with Python’s timedelta. Conflict detection was added to check for overlapping tasks. Instead of crashing, it warns the owner of this conflict so they can reassign the tasks.  Lastly, there’s a filtering feature that lets the owner view tasks by pet name and completion status, making it easier to track what’s done and what still needs to be done across multiple pets.

## Testing PawPal+
To run tests: python -m pytest
The tests cover six main areas: task behavior, sorting, recurrence, conflict detection, validation, and edge cases. They check that tasks update correctly (like marking complete and keeping fields consistent), and that scheduling respects both priority and chronological order. Recurrence tests ensure daily and weekly tasks generate new copies correctly, while one-time tasks do not, and that check_and_renew behaves as expected. They also verify that overlapping tasks are flagged while valid back-to-back tasks are allowed, and that invalid inputs raise errors. Edge cases include handling no tasks, tasks that exceed available time, removing pets or tasks, filtering by status or pet name, and ensuring explain_fit works even when nothing can be scheduled. I have a confidence level of 5 stars.