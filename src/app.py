import streamlit as st
import pandas as pd
from pathlib import Path
import os
from dotenv import load_dotenv
from modules.visualizations import create_radar_chart
from modules.scoring import calculate_position_scores
from modules.styles import apply_custom_styles
from modules.metric_selection import render_metric_weights_ui
from modules.processing import (
    load_and_process_files, 
    get_available_positions, 
    filter_players_by_position,
    aggregate_player_stats
)

load_dotenv()
PASSWORD = os.getenv("APP_PASSWORD", "PILOT26")  # Default for local dev only
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    pw = st.text_input("Type password and hit 'Enter' button on keyboard to access Best.XI:", type="password")
    if pw == PASSWORD:
        st.session_state["authenticated"] = True
        st.rerun()
    elif pw:
        st.error("Incorrect password. Please try again.")
    st.stop()

def render_header():
    logo_col1, logo_col2, logo_col3 = st.columns([1,2,1])
    with logo_col2:
        st.image("resources/best_xi_logo.png", use_container_width=True)
        st.markdown(
            '<div style="font-size: 0.7em; font-style: italic; text-align: center; margin-top: 0.5em;">'
            'Best.XI is not affiliated with or endorsed by any data provider. Users must upload data they have the legal right to use. Best.XI is a standalone decision-support tool for lineup selection.'
            '</div>',
            unsafe_allow_html=True
        )


# Tabs for navigation
TABS = ["App", "User Manual", "FAQ", "User Agreement"]
tab_app, tab_manual, tab_faq, tab_agreement = st.tabs(TABS)

with tab_app:
    render_header()
    apply_custom_styles() 

    # Step 1: Upload Player Data Files
    st.subheader("Step 1: Upload Player Data")

    uploaded_files = st.file_uploader(
        "Please drag and drop player data files here (Excel format) to begin.", 
        type=["xlsx"], accept_multiple_files=True
    )

    if uploaded_files:
        # Step 2: Process Player Data
        with st.spinner("Processing files..."):
            combined_data = load_and_process_files(uploaded_files)

        # Ensure 'Minutes Played' column exists for per 90 calculations
        if "Minutes Played" in combined_data.columns:
            combined_data = combined_data[combined_data["Minutes Played"] > 0]  # Avoid division by zero
            combined_data["Position"] = combined_data["Position"].astype(str).fillna("")
            combined_data = combined_data.explode("Position")  # Ensure multi-position players are counted correctly
        if "Position" in combined_data.columns and not combined_data["Position"].isna().all():
            combined_data["Position"] = combined_data["Position"].astype(str).fillna("")
            # get_available_positions already handles the POSITION_MAP logic internally
            unique_positions = get_available_positions(combined_data)
        else:
            unique_positions = ["No Positions Available"]
        
        # Step 2: Select Position for Comparison
        st.subheader("Step 2: Select Position for Comparison")
        selected_position = st.selectbox("Select Position", unique_positions, key="selected_position", index=0)
        # User selects a position from the dropdown (populated with valid/grouped positions)
        
        if "No Positions Available" in unique_positions:
            st.warning("No valid positions found in the data. Please check your uploaded files.")
            st.stop()
        # If no valid positions, show warning and stop

        # --- POSITION FILTERING LOGIC ---
        # Robustly detect grouped positions by checking for ' (' and group name in position_map
        filtered_data = filter_players_by_position(combined_data, selected_position)

        if filtered_data.empty:
            st.warning("No players available for this position. Please select another position.")
            st.stop()
        # If no rows after filtering, show warning and stop

        # Aggregate per 90 stats across all games where the player played this position
        # Calculate games played and minutes played at the selected position for each player
        filtered_data, numeric_cols = aggregate_player_stats(filtered_data)
        # After aggregation, filtered_data contains one row per player with mean stats for the selected position, plus games/minutes played

        # Step 3: Select Metrics
        st.subheader(f"Step 3: Select Important Metrics for {selected_position}")
        selected_metrics = st.multiselect("Select Metrics to Compare", numeric_cols, key="selected_metrics")

        # Step 4: Assign Weights (Displayed after selecting metrics)
        if selected_metrics:
            weights = render_metric_weights_ui(selected_metrics, selected_position)

            # Step 5: Select Players to Compare
            st.subheader(f"Step 5: Select Players to Compare for {selected_position}")
            selected_players = st.multiselect("Select Players", filtered_data["Player Name"].unique(), key="compare_players")

            if st.button("Perform Comparison"):
                if len(selected_players) < 2:
                    st.warning("Please select at least two players to compare.")
                else:
                    st.subheader("Comparison Results")
                    st.text("Table Ranking")
                    st.caption(f"The player with the highest score is best performer in the selected metrics for {selected_position} from the provided data.")
                    st.markdown(
                        "<small>Table shows raw per-90 stats. 'Position Score' and radar plot use normalized values (0-1) for fair comparison.</small>", unsafe_allow_html=True
                    )
                    final_data = filtered_data[filtered_data["Player Name"].isin(selected_players)]
                    relevant_metrics = list(weights.keys())

                    # Calculate Position Score using the correct 0-10 scaling
                    final_data = calculate_position_scores(final_data, weights)

                    # Rank Players by Position Score
                    ranked_data = final_data.sort_values(by="Position Score", ascending=False)
                    # Display table with position score, games/minutes played, and selected metrics
                    st.dataframe(ranked_data[["Player Name", "Position Score", "Games Played at Position", "Minutes Played at Position"] + relevant_metrics])

                    # Step 7: Visualize Player Comparisons
                    st.text("Radar Plot")
                    st.caption(f"The player that covers the most surface area is the best performer in the selected metrics for {selected_position} from the provided data.")
                    st.markdown(
                        "> **How to read this plot:** Each axis shows how a player compares to the best and worst in this group for each stat. A value closer to 1 means the player is the best in that stat among the selected players; a value closer to 0 means they are the lowest.",
                        unsafe_allow_html=True
                    )
                    radar_chart = create_radar_chart(ranked_data, selected_players, relevant_metrics)
                    st.plotly_chart(radar_chart)
                    st.markdown(
                        "<small>If all players are at 0 for a stat, it means every player had the same value for that stat in the data provided.</small>",
                        unsafe_allow_html=True
                    )
    else:
        st.info("Pending data upload...")

with tab_manual:
    render_header()
    st.markdown(Path("docs/USER_MANUAL.md").read_text(), unsafe_allow_html=True)

with tab_faq:
    render_header()
    st.markdown(Path("docs/FAQ.md").read_text(), unsafe_allow_html=True)

with tab_agreement:
    render_header()
    st.markdown(Path("docs/USER_AGREEMENT.md").read_text(), unsafe_allow_html=True)