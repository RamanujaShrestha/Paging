
import streamlit as st
import pandas as pd

from algorithms import fifo, lru, optimal
from components.memory import render_memory, render_page_table


# ==================================================
# 1. PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Paging Simulator",
    page_icon="🧠",
    layout="wide"
)


# ==================================================
# 2. HEADER
# ==================================================

st.title("🧠 Paging Simulator")
st.caption("Operating Systems | Virtual Memory Management")
st.divider()


# ==================================================
# 3. SIDEBAR
# ==================================================

st.sidebar.title("⚙️ Simulation Controls")

page = st.sidebar.radio(
    "📌 Navigation",
    [
        "🏠 Simulation",
        "📊 Analytics",
        "⚖️ Algorithm Comparison"
    ]
)

st.sidebar.divider()

frame_count = st.sidebar.slider(
    "Number of Memory Frames",
    min_value=2,
    max_value=6,
    value=3
)

reference_input = st.sidebar.text_input(
    "Page Reference String",
    "7,0,1,2,0,3,0,4,2,3,0,3,2"
)

algorithm_name = st.sidebar.selectbox(
    "Replacement Algorithm",
    ["FIFO", "LRU", "Optimal"]
)


# ==================================================
# 4. INPUT VALIDATION
# ==================================================

try:
    reference_string = [
        int(value.strip())
        for value in reference_input.split(",")
        if value.strip()
    ]

    if not reference_string:
        raise ValueError("Enter at least one page.")

    if any(number < 0 for number in reference_string):
        raise ValueError("Page numbers cannot be negative.")

except ValueError as error:
    st.error(f"Invalid reference string: {error}")
    st.stop()


# ==================================================
# 5. ALGORITHM EXECUTION
# ==================================================

algorithm_functions = {
    "FIFO": fifo,
    "LRU": lru,
    "Optimal": optimal
}

simulation = algorithm_functions[algorithm_name](
    reference_string,
    frame_count
)

total_pages = len(reference_string)

total_hits = sum(item["hit"] for item in simulation)
total_faults = sum(item["fault"] for item in simulation)

hit_ratio = total_hits / total_pages * 100
fault_ratio = total_faults / total_pages * 100


# ==================================================
# 6. COMPARISON DATA
# ==================================================

comparison_data = []

for name, function in algorithm_functions.items():

    result = function(reference_string, frame_count)

    hits = sum(item["hit"] for item in result)
    faults = sum(item["fault"] for item in result)

    comparison_data.append({
        "Algorithm": name,
        "Hits": hits,
        "Faults": faults,
        "Hit Ratio (%)": round(hits / total_pages * 100, 2),
        "Fault Ratio (%)": round(faults / total_pages * 100, 2)
    })

comparison_df = pd.DataFrame(comparison_data)

ranked_df = comparison_df.sort_values(
    by=["Faults", "Hit Ratio (%)"],
    ascending=[True, False]
).reset_index(drop=True)

ranked_df.insert(
    0,
    "Rank",
    ["🥇 1st", "🥈 2nd", "🥉 3rd"]
)

winner = ranked_df.iloc[0]


# ==================================================
# 7. SESSION STATE
# ==================================================

if "step" not in st.session_state:
    st.session_state.step = 0

if "playing" not in st.session_state:
    st.session_state.playing = False

if "playback_speed" not in st.session_state:
    st.session_state.playback_speed = 1.0

if "last_config" not in st.session_state:
    st.session_state.last_config = None

current_config = (
    tuple(reference_string),
    frame_count,
    algorithm_name
)

if st.session_state.last_config != current_config:

    st.session_state.step = 0
    st.session_state.playing = False
    st.session_state.last_config = current_config

max_step = len(simulation)

st.session_state.step = min(
    st.session_state.step,
    max_step
)


# ==================================================
# 8. SIMULATION PAGE
# ==================================================

if page == "🏠 Simulation":

    st.header("🏠 Memory Simulation")

    st.caption(
        "Visualize how pages enter and leave physical memory."
    )

    st.subheader("📊 Overall Performance")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total References", total_pages)
    col2.metric("Total Hits", total_hits)
    col3.metric("Total Faults", total_faults)
    col4.metric("Overall Hit Ratio", f"{hit_ratio:.2f}%")

    st.divider()

    st.subheader("💾 Memory Frame Visualization")

    st.write(f"Selected Algorithm: **{algorithm_name}**")

    speed = st.select_slider(
        "Animation Speed",
        options=[0.5, 0.75, 1.0, 1.5, 2.0],
        value=1.0,
        format_func=lambda value: f"{value} seconds"
    )

    st.session_state.playback_speed = speed

    # ----------------------------------------------
    # LIVE SIMULATION
    # ----------------------------------------------

    @st.fragment(
        run_every=(
            st.session_state.playback_speed
            if st.session_state.playing
            else None
        )
    )
    def simulation_animation():

        if st.session_state.playing:

            if st.session_state.step < max_step:
                st.session_state.step += 1

            if st.session_state.step >= max_step:
                st.session_state.playing = False

        step = st.session_state.step

        if step == 0:

            current_frames = []
            current_page = None
            current_status = None
            current_result = None

        else:

            current_result = simulation[step - 1]

            current_frames = current_result["frames"]
            current_page = current_result["page"]

            current_status = (
                "HIT" if current_result["hit"] else "FAULT"
            )

        # ------------------------------------------
        # LIVE PERFORMANCE CALCULATIONS
        # ------------------------------------------

        occupied_frames = len(current_frames)

        memory_utilization = (
            occupied_frames / frame_count * 100
        )

        processed_pages = simulation[:step]

        processed_faults = sum(
            item["fault"] for item in processed_pages
        )

        processed_hits = sum(
            item["hit"] for item in processed_pages
        )

        if step > 0:
            live_fault_rate = processed_faults / step * 100
            live_hit_rate = processed_hits / step * 100
        else:
            live_fault_rate = 0
            live_hit_rate = 0

        # ------------------------------------------
        # LIVE METRIC CARDS
        # ------------------------------------------

        st.subheader("📡 Live System Monitoring")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Memory Utilization",
            f"{memory_utilization:.1f}%",
            f"{occupied_frames}/{frame_count} frames"
        )

        col2.metric(
            "Live Page Fault Rate",
            f"{live_fault_rate:.2f}%"
        )

        col3.metric(
            "Live Page Hit Rate",
            f"{live_hit_rate:.2f}%"
        )

        col4.metric(
            "Processed References",
            f"{step}/{max_step}"
        )

        st.progress(memory_utilization / 100)

        st.divider()

        # ------------------------------------------
        # CURRENT MEMORY
        # ------------------------------------------

        st.subheader("🧠 Physical Memory")

        st.write(f"### Step {step} of {max_step}")

        st.progress(step / max_step)

        render_memory(
            current_frames,
            frame_count,
            current_page,
            current_status
        )

        st.subheader("📋 Page Table")

        render_page_table(
            reference_string,
            current_frames
        )

        st.divider()

        # ------------------------------------------
        # PAGE REPLACEMENT INFORMATION
        # ------------------------------------------

        st.subheader("🔄 Page Replacement Information")

        if current_result is None:

            st.info("Press Play or Next to begin.")

        elif current_result["hit"]:

            st.success(
                f"Page Hit! Page {current_result['page']} "
                "is already present in memory."
            )

        elif current_result["evicted"] is not None:

            st.warning(
                f"Page Fault! Page {current_result['evicted']} "
                f"was evicted to load Page {current_result['page']}."
            )

        else:

            st.info(
                f"Page Fault! Page {current_result['page']} "
                "was loaded into an empty memory frame."
            )

        st.divider()

        # ------------------------------------------
        # ANIMATION CONTROLS
        # ------------------------------------------

        st.subheader("🎮 Animation Controls")

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:

            if st.button(
                "▶️ Play",
                use_container_width=True,
                disabled=st.session_state.playing or step >= max_step
            ):

                st.session_state.playing = True
                st.rerun()

        with col2:

            if st.button(
                "⏸️ Pause",
                use_container_width=True,
                disabled=not st.session_state.playing
            ):

                st.session_state.playing = False
                st.rerun()

        with col3:

            if st.button(
                "⬅️ Previous",
                use_container_width=True,
                disabled=step == 0
            ):

                st.session_state.playing = False
                st.session_state.step = max(0, step - 1)
                st.rerun()

        with col4:

            if st.button(
                "Next ➡️",
                use_container_width=True,
                disabled=step >= max_step
            ):

                st.session_state.playing = False
                st.session_state.step = min(max_step, step + 1)
                st.rerun()

        with col5:

            if st.button(
                "🔄 Reset",
                use_container_width=True
            ):

                st.session_state.playing = False
                st.session_state.step = 0
                st.rerun()

        if step >= max_step and not st.session_state.playing:

            st.success("🎉 Simulation completed!")

    simulation_animation()

    st.divider()

    # ----------------------------------------------
    # PAGE HISTORY
    # ----------------------------------------------

    st.subheader("📜 Page Reference History")

    history_data = []

    for index, item in enumerate(simulation):

        history_data.append({
            "Step": index + 1,
            "Page": item["page"],
            "Frames": str(item["frames"]),
            "Result": "HIT" if item["hit"] else "FAULT",
            "Evicted Page": (
                item["evicted"]
                if item["evicted"] is not None
                else "—"
            )
        })

    st.dataframe(
        pd.DataFrame(history_data),
        use_container_width=True,
        hide_index=True
    )


# ==================================================
# 9. ANALYTICS PAGE
# ==================================================

elif page == "📊 Analytics":

    st.header("📊 Advanced Performance Analytics")

    st.caption(
        "Understand memory performance using statistical comparisons."
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total References", total_pages)
    col2.metric("Page Hits", total_hits)
    col3.metric("Page Faults", total_faults)
    col4.metric("Fault Ratio", f"{fault_ratio:.2f}%")

    st.divider()

    st.subheader("1. Page Fault Comparison")

    st.bar_chart(
        comparison_df.set_index("Algorithm")[["Faults"]]
    )

    st.divider()

    st.subheader("2. Hit Ratio Comparison")

    st.bar_chart(
        comparison_df.set_index("Algorithm")[["Hit Ratio (%)"]]
    )

    st.divider()

    st.subheader("3. Memory Performance Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Lowest Page Faults",
        comparison_df["Faults"].min()
    )

    col2.metric(
        "Average Page Faults",
        f"{comparison_df['Faults'].mean():.2f}"
    )

    col3.metric(
        "Highest Hit Ratio",
        f"{comparison_df['Hit Ratio (%)'].max():.2f}%"
    )

    st.success(
        f"Best performing algorithm: {winner['Algorithm']} "
        f"with {winner['Faults']} page faults."
    )

    st.divider()

    st.subheader("4. Detailed Algorithm Analysis")

    st.dataframe(
        comparison_df.sort_values(
            by="Faults",
            ascending=True
        ),
        use_container_width=True,
        hide_index=True
    )


# ==================================================
# 10. ALGORITHM COMPARISON PAGE
# ==================================================

elif page == "⚖️ Algorithm Comparison":

    st.header("⚖️ Algorithm Comparison")

    st.caption(
        "Compare FIFO, LRU and Optimal page replacement strategies."
    )

    st.subheader("🏆 Algorithm Performance Ranking")

    st.success(
        f"Best Algorithm: {winner['Algorithm']} "
        f"with {winner['Faults']} page faults."
    )

    st.dataframe(
        ranked_df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("📊 Hits vs Page Faults")

    st.bar_chart(
        comparison_df.set_index("Algorithm")[["Hits", "Faults"]]
    )

    st.divider()

    st.subheader("📈 Hit Ratio Comparison")

    st.bar_chart(
        comparison_df.set_index("Algorithm")[["Hit Ratio (%)"]]
    )

    st.divider()

    st.subheader("🕒 Visual Page Replacement Timeline")

    timeline_algorithm = st.selectbox(
        "Choose algorithm for timeline",
        ["FIFO", "LRU", "Optimal"],
        key="timeline_algorithm"
    )

    timeline_history = algorithm_functions[timeline_algorithm](
        reference_string,
        frame_count
    )

    timeline_rows = []

    for index, item in enumerate(timeline_history):

        row = {
            "Step": index + 1,
            "Requested Page": item["page"],
            "Result": "HIT" if item["hit"] else "FAULT",
            "Evicted Page": (
                item["evicted"]
                if item["evicted"] is not None
                else "—"
            )
        }

        for frame_index in range(frame_count):

            row[f"Frame {frame_index + 1}"] = (
                item["frames"][frame_index]
                if frame_index < len(item["frames"])
                else "Empty"
            )

        timeline_rows.append(row)

    st.dataframe(
        pd.DataFrame(timeline_rows),
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("📚 Algorithm Explanation")

    with st.expander("FIFO — First In First Out"):
        st.write(
            "FIFO replaces the page that entered memory first. "
            "It follows a queue-based replacement strategy."
        )

    with st.expander("LRU — Least Recently Used"):
        st.write(
            "LRU replaces the page that has not been used "
            "for the longest time."
        )

    with st.expander("Optimal Page Replacement"):
        st.write(
            "Optimal replaces the page whose next use is farthest "
            "in the future. It provides the theoretical minimum "
            "number of page faults when future references are known."
        )


# ==================================================
# 11. FOOTER
# ==================================================

st.divider()

st.caption(
    "Paging Simulator | FIFO • LRU • Optimal | Operating Systems Project"
)
