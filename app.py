import streamlit as st
import pawpal_system as ps
from dotenv import load_dotenv
load_dotenv()
from rag.rag_recommender import RAGTaskRecommender

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

if "owner" not in st.session_state:
    st.session_state.owner = ps.User(name="")
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "schedule_by_pet" not in st.session_state:
    st.session_state.schedule_by_pet = {}
if "ai_suggested_tasks" not in st.session_state:
    st.session_state.ai_suggested_tasks = []

st.title("🐾 PawPal+")

# ── Pet Information ──────────────────────────────────────────────────────────

st.header("Pet Information")

col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Owner name", value=st.session_state.owner.name or "")
with col2:
    pet_name = st.text_input("Pet name")

col3, col4, col5, col6 = st.columns(4)
with col3:
    species = st.selectbox("Species", ["Dog", "Cat", "Other"])
with col4:
    if species == "Other":
        custom_species = st.text_input("What type of pet?", placeholder="e.g. Rabbit, Guinea Pig, Bird")
        breed = st.text_input("Breed / Variety", placeholder="e.g. Holland Lop, Budgerigar")
    else:
        custom_species = ""
        breed = st.text_input("Breed", placeholder="e.g. Golden Retriever, Persian")
with col5:
    age = st.slider("Age (years)", 0, 20, 3)
with col6:
    available_time = st.slider("Available time per day (min)", 30, 240, 120)

# Resolve the actual species to use
actual_species = custom_species.strip() if species == "Other" and custom_species.strip() else species

if st.button("Add Pet"):
    if not pet_name.strip():
        st.warning("Please enter a pet name.")
    elif species == "Other" and not custom_species.strip():
        st.warning("Please specify what type of pet it is.")
    else:
        st.session_state.owner.name = owner_name or "Owner"
        existing_names = [p.name.lower() for p in st.session_state.owner.view_pets()]
        if pet_name.lower() in existing_names:
            st.warning(f"{pet_name} is already added.")
        else:
            pet = ps.Pet(name=pet_name, species=actual_species.lower(), age=age)
            pet.breed = breed
            pet.available_time = available_time
            st.session_state.owner.add_pet(pet)
            st.success(f"Added {pet_name} the {breed or species}!")

current_pets = st.session_state.owner.view_pets()
if current_pets:
    cols = st.columns(len(current_pets))
    for i, p in enumerate(current_pets):
        with cols[i]:
            breed_label = getattr(p, "breed", "") or p.species
            st.markdown(f"**{p.name}** · {breed_label} · {p.age} yr")

    remove_name = st.selectbox("Remove a pet", [""] + [p.name for p in current_pets])
    if st.button("Remove pet") and remove_name:
        st.session_state.owner.remove_pet(remove_name)
        st.session_state.tasks = [t for t in st.session_state.tasks if t.get("pet") != remove_name]
        st.success(f"Removed {remove_name}.")
        st.rerun()

st.divider()

# ── Tasks ────────────────────────────────────────────────────────────────────

st.header("Tasks")

pets = st.session_state.owner.view_pets()
pet_names = [p.name for p in pets]

if not pet_names:
    st.info("Add a pet above before adding tasks.")
else:
    # ── AI Suggestion ──
    st.subheader("Ask AI for a Schedule Suggestion")
    st.caption("Select your pet and preferred time of day — AI will suggest the best tasks and times based on your pet's needs.")

    col_a, col_b = st.columns(2)
    with col_a:
        ai_pet = st.selectbox("Select pet", pet_names, key="ai_pet_select")
    with col_b:
        time_of_day = st.selectbox(
            "Preferred time of day",
            ["Morning", "Afternoon", "Evening", "All day"],
            key="time_of_day"
        )

    if st.button("Get AI Suggestions", type="primary"):
        selected_pet = next((p for p in pets if p.name == ai_pet), None)
        if selected_pet:
            with st.spinner("Generating personalized schedule..."):
                try:
                    recommender = RAGTaskRecommender()
                    breed_info = getattr(selected_pet, "breed", "") or selected_pet.species
                    avail = getattr(selected_pet, "available_time", 120)
                    constraints = (
                        f"{avail} minutes available daily, "
                        f"preferred time of day: {time_of_day}, "
                        f"breed: {breed_info}"
                    )
                    ai_tasks = recommender.recommend_tasks(selected_pet, owner_constraints=constraints)
                    if hasattr(recommender, "_rate_limit_message"):
                        st.warning(f"⚠️ {recommender._rate_limit_message}")
                    st.session_state.ai_suggested_tasks = [
                        {
                            "pet": ai_pet,
                            "title": t.name,
                            "duration_minutes": t.duration,
                            "priority": t.priority,
                            "start_time": t.start_time,
                            "reasoning": getattr(t, "reasoning", ""),
                        }
                        for t in ai_tasks
                    ]
                except Exception as e:
                    st.error(f"AI suggestion failed: {e}")

    if st.session_state.ai_suggested_tasks:
        st.markdown("**Suggested tasks:**")
        priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}
        for t in st.session_state.ai_suggested_tasks:
            st.write(
                f"{priority_emoji.get(t['priority'], '')} **{t['title']}** "
                f"— {t['start_time']} · {t['duration_minutes']} min · {t['priority']}"
            )
            if t.get("reasoning"):
                st.caption(t["reasoning"])

        if st.button("Add AI suggestions to task list"):
            for t in st.session_state.ai_suggested_tasks:
                st.session_state.tasks.append(t)
            count = len(st.session_state.ai_suggested_tasks)
            st.session_state.ai_suggested_tasks = []
            st.success(f"Added {count} tasks to your list!")
            st.rerun()

    st.divider()

    # ── Manual Tasks ──
    st.subheader("Add Tasks Manually")

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        task_pet = st.selectbox("For pet", pet_names, key="manual_pet")
    with col2:
        task_title = st.text_input("Task title", value="Morning walk")
    with col3:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col4:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    with col5:
        start_time = st.text_input("Start time (HH:MM)", value="08:00")

    if st.button("Add task"):
        st.session_state.tasks.append({
            "pet": task_pet,
            "title": task_title,
            "duration_minutes": int(duration),
            "priority": priority,
            "start_time": start_time,
        })
        st.success(f"Added: {task_title}")
        st.rerun()

# Task list
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

    task_options = [
        f"{t.get('pet', '?')} — {t.get('title', '?')} ({t.get('start_time', '?')})"
        for t in st.session_state.tasks
    ]
    remove_task = st.selectbox("Remove a task", [""] + task_options)
    if st.button("Remove task") and remove_task:
        st.session_state.tasks.pop(task_options.index(remove_task))
        st.success("Task removed.")
        st.rerun()
elif pet_names:
    st.info("No tasks yet. Use AI suggestions or add one manually above.")

st.divider()

# ── Build Schedule ───────────────────────────────────────────────────────────

st.subheader("Build Schedule")
time_available = st.number_input("Minutes available today", min_value=1, max_value=480, value=60)

if st.button("Generate schedule"):
    pets = st.session_state.owner.view_pets()
    if not pets:
        st.warning("Add a pet first.")
    elif not st.session_state.tasks:
        st.warning("Add at least one task first.")
    else:
        pet_lookup = {p.name: p for p in pets}
        for pet in pets:
            pet.tasks.clear()
        for t in st.session_state.tasks:
            target_pet = pet_lookup.get(t.get("pet"))
            if target_pet is None:
                continue
            target_pet.add_task(ps.Task(
                name=t["title"],
                priority=t["priority"],
                duration=t["duration_minutes"],
                start_time=t.get("start_time", "00:00"),
            ))
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

if st.session_state.schedule_by_pet:
    priority_badge = {"high": "🔴 High", "medium": "🟡 Medium", "low": "🟢 Low"}
    st.subheader("Today's Schedule")
    all_rows = []
    for pname, data in st.session_state.schedule_by_pet.items():
        for t in data["tasks"]:
            all_rows.append({
                "Pet": pname,
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
    for pname, data in st.session_state.schedule_by_pet.items():
        if data["warnings"]:
            st.markdown(f"**⚠️ Conflicts for {pname}**")
            for w in data["warnings"]:
                st.warning(w.replace("WARNING: ", "").replace("overlaps with", "conflicts with"))
            st.info("Tip: Adjust start times so tasks no longer overlap.")
        else:
            st.success(f"No conflicts for {pname}!")
        with st.expander(f"Why were these tasks chosen for {pname}?", expanded=False):
            st.markdown(data["explanation"])

st.markdown("---")
st.caption("Built with Streamlit, Gemini AI, and sentence-transformers for RAG")
