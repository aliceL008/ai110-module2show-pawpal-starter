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

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
