# PawPal+ Project Reflection

## 1. System Design
1. User should be able to create owner & pet profile
2. Create tasks that adds the duration and priority of the pet 
3. Use the tasks to create a schedule list for daily plans and explain why this fits 
**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

The main objects needed are User, Pet, Tasks, and Scheduler. The User class should be able to add, remove, or view their pets using their name and list of pets. The Pet class should be able to add, remove, or view tasks using name, species, age, and list of tasks. The Task class should be able to add the durations and priorities using the name of the tasks and level of priorities. The Scheduler class should be able to make the schedule, sort it by priority, fit the times, and explain why it fits using the list of tasks and the time available. 

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
Yes, I added a method to allow the owner to view all the tasks as it is important for them to know what was done for their pets. I also added a method to mark the task as complete as it is important to let the owner know what has been done. An explanation of why the task was skipped was also added for the owners to see the constraints limiting that task. 

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?
My scheduler considers time, priority, ordering by start time, recurrence, conflicts, and completion. The main ones are time and priority, because tasks are picked based on priority and only if they fit in the available time. It also checks start times to order tasks correctly and makes sure tasks don’t overlap. Recurrence and completion make sure new tasks only show up after the old ones are done, so there are no duplicates. I chose time and priority as the most important because they directly affect what gets scheduled. Since time is limited, higher priority tasks should be done first. The other constraints like conflicts and completion just help make the schedule realistic, making sure tasks don’t overlap and new ones don’t repeat before finishing old ones.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for The scheduler uses a greedy approach where it picks tasks in priority order and stops when the next task doesn’t fit. It doesn’t look ahead to see if a smaller, lower-priority task could better use the remaining time. For example, if there are 20 minutes left and the next high-priority task takes 30 minutes, it skips it and stops, even if a 15-minute low-priority task could fit. This tradeoff is reasonable for a pet care schedule because completing the most important tasks matters more than perfectly filling time. A pet owner would rather ensure feeding or medication is done, even if some time is unused, than risk skipping essential care. The greedy approach is also simple and easy to explain, which helps make the system more understandable and trustworthy for users.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?
I used AI throughout the project for test planning, debugging, and UI development. Early on, I asked it to identify edge cases for a pet scheduler, like pets with no tasks or tasks at the same time, which helped shape my test suite before I even started writing tests. During debugging, it helped me figure out why test_check_and_renew_generates_next_occurrence_after_all_complete was failing—it turned out the schedule included both the old completed task and the new renewed one, so using index 0 wasn’t reliable. I also used it to update app.py and connect the Scheduler logic to the Streamlit UI, including sorting, conflict warnings, and displaying schedules per pet. The most helpful prompts were specific and based on my actual code. For example, asking “is the bug in my test or in pawpal_system.py?” with the error message gave a clear explanation and root cause. Asking for edge cases within the scheduler context gave more useful results than general questions. More detailed prompts like “use st.success, st.warning, and st.table to display conflicts in a user-friendly way” worked much better than vague ones like “improve the UI,” since they gave clearer direction and context.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
When AI generated the initial test for check_and_renew, it used renewed = new_schedule[0] and then asserted that renewed.status == "incomplete". When I ran the test, it failed. Instead of immediately applying the suggested fix, I looked into check_and_renew() to understand what was actually happening. I found that the method rebuilds self.tasks using self.user.get_all_tasks(), which means the schedule includes both the original completed task and the newly renewed one. Since make_schedule() sorts by priority and start time, and both tasks had the same values, their order wasn’t guaranteed. After tracing the logic step by step, I realized the issue wasn’t just the test—it was assuming a fixed position in a list that isn’t deterministic. Once I understood that, it made more sense to filter for the incomplete renewed task instead of relying on new_schedule[0].

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?
The tests covered five core behaviors: task status (default incomplete, marking complete, idempotency), sorting (chronological order and priority ranking), recurrence (daily/weekly renewal logic and correct triggering of check_and_renew, with one-time tasks not recurring), conflict detection (overlapping and same-time tasks flagged, back-to-back tasks allowed), and input validation (rejecting invalid durations and priorities). These tests were important because sorting and conflict detection directly affect what the user sees, so errors there would immediately make the schedule misleading. Recurrence is more complex since it depends on multiple classes and only triggers when all tasks are complete, so it’s easy to break silently. Validation ensures invalid inputs don’t corrupt the schedule or fail quietly in the UI.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?
I’m very confident in the core functionality because there are extensive tests covering priority sorting, time budget fitting, conflict detection, and recurrence, including both success and failure cases. However, there are still some edge cases I would want to verify further. These include malformed start_time inputs that could break _to_minutes() without clear errors, and interactions between multiple pets to ensure conflicts don’t leak across schedules. I would also test check_and_renew() for weekly tasks that were never completed to confirm it doesn’t incorrectly renew them. Additionally, I’d check repeated schedule generation without resetting state to make sure tasks don’t accumulate and distort the time budget over time.
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I am very satisfied that I was able to design and implement a strong set of tests and methods that reflect real-world pet owner needs, which helped make the system more practical and convenient. This process also helped me think critically about what features actually matter in a scheduling system. I was able to uncover many bugs during development and use AI as a tool to help surface and debug issues more efficiently.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
If I had another iteration, I would redesign how the Scheduler accesses tasks. Taking a snapshot at initialization caused issues, especially in check_and_renew(), where I had to manually refresh self.tasks. A better design would be to fetch tasks dynamically from pets instead. I would also separate detect_conflicts() from make_schedule() since rebuilding the schedule repeatedly inside conflict detection is redundant and makes the system less clean and harder to maintain.
**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
The most important lesson I learned is that good system design depends heavily on strong test coverage to support debugging and prevent hidden issues. I also learned that while AI is helpful for debugging and generating ideas, it requires persistence and careful questioning to fully understand why a solution works and how it can be improved.
