import streamlit as st
import pawpal_system as ps

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])


if "owner" not in st.session_state:
    st.session_state.owner = ps.User(name=owner_name)

if st.button("Add pet"):
    existing_names = [p.name.lower() for p in st.session_state.owner.view_pets()]
    if pet_name.lower() in existing_names:
        st.warning(f"{pet_name} is already added.")
    else:
        pet = ps.Pet(name=pet_name, species=species, age=1)
        st.session_state.owner.add_pet(pet)
        st.success(f"Added {pet_name} the {species}!")

if st.session_state.owner.view_pets():
    st.write("Pets:", [p.name for p in st.session_state.owner.view_pets()])
    remove_name = st.selectbox("Remove a pet", [""] + [p.name for p in st.session_state.owner.view_pets()])
    if st.button("Remove pet") and remove_name:
        st.session_state.owner.remove_pet(remove_name)
        st.session_state.tasks = [t for t in st.session_state.tasks if t.get("pet") != remove_name]
        st.success(f"Removed {remove_name}.")
        st.rerun()

st.divider()

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

pets = st.session_state.owner.view_pets()
pet_names = [p.name for p in pets]

if not pet_names:
    st.info("Add a pet above before adding tasks.")
else:
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        task_pet = st.selectbox("For pet", pet_names)
    with col2:
        task_title = st.text_input("Task title", value="Morning walk")
    with col3:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col4:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    with col5:
        start_time = st.text_input("Start time (HH:MM)", value="08:00")

    if st.button("Add task"):
        st.session_state.tasks.append(
            {"pet": task_pet, "title": task_title, "duration_minutes": int(duration), "priority": priority, "start_time": start_time}
        )

if st.session_state.tasks:
    tasks_by_pet = {}
    for t in st.session_state.tasks:
        tasks_by_pet.setdefault(t.get("pet", "Unknown"), []).append(t)
    for pet_label, pet_tasks in tasks_by_pet.items():
        st.markdown(f"**{pet_label}**")
        st.table([
            {"Task": t["title"], "Start": t["start_time"], "Duration (min)": t["duration_minutes"], "Priority": t["priority"]}
            for t in pet_tasks
        ])

    task_options = [f"{t.get('pet', '?')} — {t.get('title', '?')} ({t.get('start_time', '?')})" for t in st.session_state.tasks]
    remove_task = st.selectbox("Remove a task", [""] + task_options)
    if st.button("Remove task") and remove_task:
        idx = task_options.index(remove_task)
        st.session_state.tasks.pop(idx)
        st.success("Task removed.")
        st.rerun()
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
time_available = st.number_input("Minutes available today", min_value=1, max_value=480, value=60)

if "schedule_by_pet" not in st.session_state:
    st.session_state.schedule_by_pet = {}  # {pet_name: [Task, ...]}

if st.button("Generate schedule"):
    pets = st.session_state.owner.view_pets()
    if not pets:
        st.warning("Add a pet first.")
    elif not st.session_state.tasks:
        st.warning("Add at least one task first.")
    else:
        pet_lookup = {p.name: p for p in pets}

        # Clear old pet tasks before reassigning
        for pet in pets:
            pet.tasks.clear()

        # Assign tasks to the correct pet
        for t in st.session_state.tasks:
            target_pet = pet_lookup.get(t.get("pet"))
            if target_pet is None:
                continue
            task = ps.Task(
                name=t["title"],
                priority=t["priority"],
                duration=t["duration_minutes"],
                start_time=t.get("start_time", "00:00"),
            )
            target_pet.add_task(task)

        # Build and store the schedule per pet so completion state persists
        st.session_state.schedule_by_pet = {}
        for pet in pets:
            if not pet.view_tasks():
                continue
            pet_user = ps.User(name=st.session_state.owner.name)
            pet_user.add_pet(pet)
            scheduler = ps.Scheduler(user=pet_user, time_available=int(time_available))
            st.session_state.schedule_by_pet[pet.name] = {
                "tasks": scheduler.make_schedule(),
                "warnings": scheduler.detect_conflicts(),
                "explanation": scheduler.explain_fit(),
            }

# Display the stored schedule (persists across reruns so mark-complete works)
if st.session_state.schedule_by_pet:
    priority_badge = {"high": "🔴 High", "medium": "🟡 Medium", "low": "🟢 Low"}
    st.subheader("Today's Schedule")

    all_rows = []
    for pet_name, data in st.session_state.schedule_by_pet.items():
        for t in data["tasks"]:
            all_rows.append({
                "Pet": pet_name,
                "Task": t.name,
                "Start": t.start_time,
                "Duration (min)": t.duration,
                "Priority": priority_badge.get(t.priority, t.priority),
            })

    if all_rows:
        all_rows.sort(key=lambda r: r["Start"])
        st.table(all_rows)
    else:
        st.info("No tasks fit in the available time.")

    st.divider()

    # Conflicts and explanations still per pet
    for pet_name, data in st.session_state.schedule_by_pet.items():
        warnings = data["warnings"]
        if warnings:
            st.markdown(f"**⚠️ Conflicts for {pet_name}**")
            for w in warnings:
                friendly = w.replace("WARNING: ", "").replace("overlaps with", "conflicts with")
                st.warning(friendly)
            st.info("Tip: Adjust the start time of one of the conflicting tasks so they no longer overlap.")
        else:
            st.success(f"No conflicts for {pet_name}!")

        with st.expander(f"Why were these tasks chosen for {pet_name}?", expanded=False):
            st.markdown(data["explanation"])
