import streamlit as st
import pandas as pd
from modules.processing import load_and_process_files
from modules.visualizations import create_radar_chart

# Streamlit app
st.title("Best.XI: Player Data Processing and Comparison")

# Step 1: Upload Player Data Files
st.subheader("Step 1: Upload Player Data Files")

uploaded_files = st.file_uploader(
    "Drag and drop player data files here (Excel format)", 
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
        unique_positions = sorted(set(
            pos.strip() for positions in combined_data["Position"].dropna() for pos in positions.split(",") if pos.strip()
        ))
        
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
    
        unique_positions = sorted(set(
            pos.strip() for positions in combined_data["Position"].dropna() for pos in positions.split(",") if pos.strip()
        ) | set(
            f"{group_name} ({'/'.join(grouped_positions)})" for group_name, grouped_positions in position_map.items()
        ))

    else:
        unique_positions = ["No Positions Available"]  # Placeholder if no positions exist
    
    # Step 3: Select Position for Comparison
    st.subheader("Step 2: Select Position to Compare")
    selected_position = st.selectbox("Select Position", unique_positions, key="selected_position")
    
    if "No Positions Available" in unique_positions:
        st.warning("No valid positions found in the data. Please check your uploaded files.")
        st.stop()

    # Filter data based on selected position
    filtered_data = combined_data[combined_data["Position"] == selected_position]
    
    # Aggregate per 90 stats across all games where the player played this position
    numeric_cols = filtered_data.select_dtypes(include=["number"]).columns.tolist()
    filtered_data = filtered_data.groupby("Player Name")[numeric_cols].mean().reset_index()

    # Step 4: Select Metrics
    st.subheader(f"Step 3: Select Important Metrics for {selected_position}")
    selected_metrics = st.multiselect("Select Metrics to Compare", numeric_cols, key="selected_metrics")

    # Step 5: Assign Weights (Displayed after selecting metrics)
    if selected_metrics:
        st.subheader(f"Step 4: Rank Metrics Importance (1-10) for {selected_position}.")
        weights = {}
        cols = st.columns(min(3, len(selected_metrics)))  # Distribute weights across multiple columns
        for idx, metric in enumerate(selected_metrics):
            with cols[idx % 3]:
                weights[metric] = st.number_input(
                    f"{metric}", min_value=1, max_value=10, value=5, step=1, key=f"weight_{metric}", format='%d'
                )

        # Step 6: Select Players to Compare
        st.subheader("Step 5: Select Players to Compare")
        selected_players = st.multiselect("Select Players", filtered_data["Player Name"].unique(), key="compare_players")

        if st.button("Perform Comparison"):
            if len(selected_players) < 2:
                st.warning("Please select at least two players to compare.")
            else:
                st.subheader("Comparison Results")
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
                st.subheader("Visualize Player Comparisons")
                radar_chart = create_radar_chart(ranked_data, selected_players, relevant_metrics)
                st.plotly_chart(radar_chart)
else:
    st.info("Please upload player data files to begin.")

