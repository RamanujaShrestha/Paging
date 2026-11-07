
import streamlit as st
import pandas as pd


def render_memory(frames, frame_count, current_page=None, status=None):

    st.subheader("🧠 Physical Memory")

    st.caption(f"Memory capacity: {frame_count} frames")

    columns = st.columns(frame_count)

    for index in range(frame_count):

        with columns[index]:

            if index < len(frames):
                page = frames[index]

                st.markdown(
                    f"""
                    <div style="
                        background: #172554;
                        border: 2px solid #3b82f6;
                        border-radius: 12px;
                        padding: 20px 8px;
                        text-align: center;
                        min-height: 115px;
                    ">
                        <div style="color:#93c5fd;font-size:13px;">
                            FRAME {index + 1}
                        </div>
                        <div style="
                            color:white;
                            font-size:30px;
                            font-weight:bold;
                            margin-top:12px;
                        ">
                            {page}
                        </div>
                        <div style="color:#93c5fd;font-size:11px;">
                            PAGE LOADED
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:
                st.markdown(
                    f"""
                    <div style="
                        background: #1e293b;
                        border: 1px dashed #64748b;
                        border-radius: 12px;
                        padding: 20px 8px;
                        text-align: center;
                        min-height: 115px;
                    ">
                        <div style="color:#94a3b8;font-size:13px;">
                            FRAME {index + 1}
                        </div>
                        <div style="
                            color:#64748b;
                            font-size:26px;
                            margin-top:12px;
                        ">
                            —
                        </div>
                        <div style="color:#94a3b8;font-size:11px;">
                            EMPTY
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    if current_page is not None:

        st.write(f"**Requested Page:** {current_page}")

    if status == "HIT":
        st.success("🟢 PAGE HIT — Page already exists in memory.")

    elif status == "FAULT":
        st.error("🔴 PAGE FAULT — Page loaded into memory.")


def render_page_table(reference_string, frames):

    st.divider()

    st.subheader("📋 Page Table")

    all_pages = sorted(set(reference_string))

    page_table = []

    for page in all_pages:

        if page in frames:

            frame_number = frames.index(page) + 1
            status = "PRESENT"

        else:

            frame_number = "—"
            status = "ABSENT"

        page_table.append({
            "Page Number": page,
            "Frame Number": frame_number,
            "Status": status
        })

    df = pd.DataFrame(page_table)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
