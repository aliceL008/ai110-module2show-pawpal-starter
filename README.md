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
PawPal+ was extended with features to make the scheduler more practical and easier to use. Tasks now include:
1. Time field so the daily plan can be shown in chronological order while still considering priority
2. Recurring tasks can be set as daily or weekly, and once all tasks are completed, the scheduler automatically generates the next plan using updated dates with Python’s timedelta. 
3. Conflict detection was added to check for overlapping tasks. Instead of crashing, it warns the owner of this conflict so they can reassign the tasks.  4. Filtering feature that lets the owner view tasks by pet name and completion status, making it easier to track what’s done and what still needs to be done across multiple pets.

## Testing PawPal+
To run tests: python -m pytest

The tests cover six main areas: task behavior, sorting, recurrence, conflict detection, validation, and edge cases. 
They check that tasks update correctly (like marking complete and keeping fields consistent), and that scheduling respects both priority and chronological order. Recurrence tests ensure daily and weekly tasks generate new copies correctly, while one-time tasks do not, and that check_and_renew behaves as expected. 
They verify that overlapping tasks are flagged while valid back-to-back tasks are allowed, and that invalid inputs raise errors. It also handle edge cases where no tasks are assigned, tasks that exceed available time, removing pets or tasks, filtering by status or pet name, and ensuring explain_fit works even when nothing can be scheduled. I have a confidence level of 5 stars.

## Features
1. Priority-based scheduling — tasks are ranked high → medium → low and greedily selected to fill the available time budget before lower-priority tasks are considered
2. Chronological sorting — the final schedule is sorted by start_time so the day's tasks appear in the order they should happen
3. Time budget fitting — tasks that would exceed the remaining available minutes are skipped; the scheduler fits as many high-priority tasks as possible within the limit
4. Conflict detection — pairwise comparison of all scheduled tasks flags any whose time windows overlap using the condition a_start < b_end and b_start < a_end
5. Daily recurrence — marking a daily task complete generates a fresh copy due the next day via next_occurrence()
Weekly recurrence — same as daily but the follow-up task is due 7 days later
6. Auto-renewal — once every task in the schedule is marked complete, check_and_renew() automatically rebuilds the schedule from recurring tasks
Per-pet scheduling — each pet gets its own independent schedule, time budget, and conflict check
7. Task filtering — tasks can be filtered by completion status, pet name, or both
Schedule explanation — explain_fit() reports which tasks were selected and why, and lists any skipped due to time constraints


## DEMO
Running the demo: python main.py

<a href="/course_images/ai110/demo.png" target="_blank"><img src='/course_images/ai110/demo.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>.