import streamlit as st
import pandas as pd
from modules.processing import load_and_process_files
from modules.visualizations import create_radar_chart

# Password protection
PASSWORD = "PILOT25"
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

# Streamlit app
st.markdown(
    """
    <style>
    .stApp {background-color: #e0e0e0; color: #222 !important;}
    .stMarkdown, .css-10trblm, .css-1v0mbdj, .css-1d391kg, .css-1cpxqw2 {color: #222 !important;}
    .stMarkdownContainer {color: #000 !important;}
    .stAlert {background-color: #e3f0ff !important; color: #111 !important; font-weight: bold;}
    .stAlert > div {color: #111 !important;}
    .stFileUploader label {color: #222 !important;}
    .stSelectbox label, .stMultiSelect label, .stSelectbox label span, .stMultiSelect label span {color: #222 !important;}
    .stDataFrame .css-1vzeuhh, .stDataFrame .css-12w0qpk {color: #222 !important;}
    .stDataFrame div, .stDataFrame span {color: #000 !important;}
    .stDataFrame th, .stDataFrame td {color: inherit !important;}
    .stFileUploader .css-1aehpvj, .stFileUploader .st-badge, .stFileUploader .badge, .stFileUploader span[style*="background"], .stFileUploader div[style*="background"] {
        color: #111 !important;
        background: #e0e0e0 !important;
    }
    st-emotion-cache-qoz3f2, st-emotion-cache-qoz3f2 p {
        color: #000 !important;
    }
    
    .stFileUploader .st-emotion-cache-c8ta4l {
        color: #808080 !important;
    }

    .st-emotion-cache-qoz3f2 p, .st-emotion-cache-qoz3f2 {color: #000 !important;}
    .st-emotion-cache-1weic72 {color: #000 !important;}
    .st-emotion-cache-ovf5rk p, .st-emotion-cache-ovf5rk {color: #fff !important;}
    .st-emotion-cache-1u2dcfn {color: #fff !important;}
    .st-emotion-cache-1ucesps svg {color: #fff !important;}
    th[role="columnheader"] {color: #fff !important; font-weight: bold !important;}
    .st-emotion-cache-ah6jdd {color: #000 !important;}
    .st-emotion-cache-y4bq5x {color: #000 !important;}

    </style>
    """,
    unsafe_allow_html=True
)

# Center the logo using Streamlit's columns
logo_col1, logo_col2, logo_col3 = st.columns([1,2,1])
with logo_col2:
    st.image("best_xi_logo.png", use_container_width=True)
    st.markdown(
        '<div style="font-size: 0.7em; font-style: italic; text-align: center; margin-top: 0.5em;">'
        'Best.XI is not affiliated with or endorsed by any data provider. Users must upload data they have the legal right to use. Best.XI is a standalone decision-support tool for lineup selection.'
        '</div>',
        unsafe_allow_html=True
    )

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
        position_map = {
            "ST": ["CF", "ST"],
            "WG": ["LW", "RW", "LWF", "RWF"],
            "CAM/10": ["AMF", "LAMF", "RAMF"],
            "CDM/6": ["DMF", "LDMF", "RDMF"],
            "CM/8": ["CMF", "LCMF", "RCMF", "LCMF3", "RCMF3"],
            "FB": ["LB", "RB", "LWB", "RWB", "LB5", "RB5"],
            "CB": ["CB", "LCB", "RCB", "LCB3", "RCB3"],
            "GK": ["GK"]
        }
    
        # Get unique positions from the data
        data_positions = set(
            pos.strip() for positions in combined_data["Position"].dropna() 
            for pos in positions.split(",") if pos.strip()
        )
        
        # Create final position list including both individual and grouped positions
        unique_positions = set()
        for group_name, grouped_positions in position_map.items():
            # Find players for each position in the group
            players_in_group = combined_data[
                combined_data["Position"].apply(lambda x: any(pos in x for pos in grouped_positions))
            ]
            if not players_in_group.empty:
                unique_positions.add(f"{group_name} ({'/'.join(grouped_positions)})")
                unique_positions.update(pos for pos in grouped_positions if not combined_data[combined_data["Position"].str.contains(pos)].empty)
        # Only keep positions with at least one player
        unique_positions = sorted(unique_positions)

    else:
        unique_positions = ["No Positions Available"]  # Placeholder if no positions exist
    
    # Step 2: Select Position for Comparison
    st.subheader("Step 2: Select Position for Comparison")
    selected_position = st.selectbox("Select Position", unique_positions, key="selected_position", index=0)
    
    if "No Positions Available" in unique_positions:
        st.warning("No valid positions found in the data. Please check your uploaded files.")
        st.stop()

    # Filter data based on selected position
    if selected_position in position_map:
        # Grouped position: filter for any of the mapped positions
        group_positions = position_map[selected_position.split(" (")[0]]
        filtered_data = combined_data[combined_data["Position"].apply(lambda x: any(pos in x for pos in group_positions))]
    else:
        # Individual position
        filtered_data = combined_data[combined_data["Position"].str.contains(selected_position)]

    if filtered_data.empty:
        st.warning("No players available for this position. Please select another position.")
        st.stop()

    # Aggregate per 90 stats across all games where the player played this position
    numeric_cols = filtered_data.select_dtypes(include=["number"]).columns.tolist()
    filtered_data = filtered_data.groupby("Player Name")[numeric_cols].mean().reset_index()

    # Step 3: Select Metrics
    st.subheader(f"Step 3: Select Important Metrics for {selected_position}")
    selected_metrics = st.multiselect("Select Metrics to Compare", numeric_cols, key="selected_metrics")

    # Step 4: Assign Weights (Displayed after selecting metrics)
    if selected_metrics:
        st.subheader(f"Step 4: Rank Metrics Importance (1-10) for {selected_position}.")
        weights = {}
        cols = st.columns(min(3, len(selected_metrics)))  # Distribute weights across multiple columns
        for idx, metric in enumerate(selected_metrics):
            with cols[idx % 3]:
                weights[metric] = st.number_input(
                    f"{metric}", min_value=1, max_value=10, value=5, step=1, key=f"weight_{metric}", format='%d'
                )

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

                # Calculate Position Score
                final_data["Position Score"] = final_data.apply(
                    lambda row: sum(row[metric] * weights[metric] for metric in weights if metric in row), axis=1
                )

                # Rank Players by Position Score
                ranked_data = final_data.sort_values(by="Position Score", ascending=False)
                st.dataframe(ranked_data[["Player Name", "Position Score"] + relevant_metrics])

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

