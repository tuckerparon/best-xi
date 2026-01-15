import pandas as pd
from modules.config import POSITION_MAP

def get_available_positions(df):
    """Generates a list of unique and grouped positions available in the data."""
    if "Position" not in df.columns or df["Position"].isna().all():
        return ["No Positions Available"]

    unique_positions = set()
    
    for group_name, grouped_positions in POSITION_MAP.items():
        group_set = set(grouped_positions)
        
        # Check if any players exist for this group
        players_in_group = df[
            df["Position"].apply(
                lambda x: isinstance(x, str) and any(
                    pos in group_set for pos in [p.strip() for p in x.split(",")]
                )
            )
        ]
        
        if not players_in_group.empty:
            # Add the group name option
            unique_positions.add(f"{group_name} ({'/'.join(grouped_positions)})")
            
            # Add individual positions that exist within that group
            for pos in grouped_positions:
                has_pos = not df[
                    df["Position"].apply(
                        lambda x: isinstance(x, str) and pos in [p.strip() for p in x.split(",")]
                    )
                ].empty
                if has_pos:
                    unique_positions.add(pos)
                    
    return sorted(list(unique_positions))


def filter_players_by_position(df, selected_position):
    """
    Filters the dataframe based on the selected position string.
    Handles both grouped positions (e.g., 'ST (CF/ST)') and individual positions.
    """
    if not isinstance(selected_position, str) or "No Positions Available" in selected_position:
        return df.iloc[0:0] # Return empty dataframe

    # Check if it's a grouped position from our map
    if " (" in selected_position:
        group_name = selected_position.split(" (")[0]
        if group_name in POSITION_MAP:
            group_positions = set(POSITION_MAP[group_name])
            return df[
                df["Position"].apply(
                    lambda x: isinstance(x, str) and any(
                        pos in group_positions for pos in [p.strip() for p in x.split(",")]
                    )
                )
            ]

    # Otherwise, treat as an individual position match
    return df[
        df["Position"].apply(
            lambda x: isinstance(x, str) and selected_position in [p.strip() for p in x.split(",")]
        )
    ]


def aggregate_player_stats(df):
    """
    Aggregates stats across all games for each player.
    Calculates mean for numeric metrics and totals for games/minutes.
    """
    # 1. Count games played and sum minutes played
    games_played = df.groupby("Player Name").size().rename("Games Played at Position")
    
    # Handle potential casing differences in column names
    minutes_col = next((c for c in df.columns if c.lower() == "minutes played"), "Minutes Played")
    minutes_played = df.groupby("Player Name")[minutes_col].sum().rename("Minutes Played at Position")
    
    # 2. Get numeric columns for averaging
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    
    # 3. Aggregate means
    df_agg = df.groupby("Player Name")[numeric_cols].mean().reset_index()
    
    # 4. Merge totals back in
    df_agg = df_agg.merge(games_played, on="Player Name").merge(minutes_played, on="Player Name")
    
    return df_agg, numeric_cols


def process_formatting_split(df):
    """
    Adjust column names for formatting where metrics have a "total/detail" structure.
    Detects patterns based on "/" and pairs appropriately.
    """
    updated_columns = []
    skip_next = False
    
    for i, col in enumerate(df.columns):
        if skip_next:
            skip_next = False
            continue
        
        if " / " in col and i + 1 < len(df.columns) and "Unnamed" in df.columns[i + 1]:
            # Split the column by " / " and create total and detailed versions
            metric_base, detail = col.split(" / ")
            updated_columns.append(f"{metric_base} (total)")
            updated_columns.append(f"{metric_base} ({detail})")
            skip_next = True  # Skip the next column as it has been paired
        else:
            updated_columns.append(col)
    
    # Ensure the final column count matches
    while len(updated_columns) < len(df.columns):
        updated_columns.append(df.columns[len(updated_columns)])
    
    # Update the DataFrame with the new column names
    df.columns = updated_columns
    
    # Drop columns that represent the minute of the card, not the count
    for col_to_drop in ["Red card", "Yellow card"]:
        if col_to_drop in df.columns:
            df = df.drop(columns=[col_to_drop])
    
    # Add percentage columns
    percentage_columns = {}
    for col in df.columns:
        if " (total)" in col:
            base_name = col.replace(" (total)", "")
            for detail_col in df.columns:
                if detail_col.startswith(base_name) and detail_col != col:
                    percent_col = f"% {detail_col}"
                    df[percent_col] = (df[detail_col] / df[col]) * 100
                    df[percent_col] = df[percent_col].fillna(0)  # Replace NaNs with 0
    
    return df

def load_and_process_files(file_paths):
    """Load multiple player files, preprocess them, and combine into a single DataFrame."""
    dataframes = []
    for file in file_paths:
        # Extract player name from the file name
        player_name = file.name.split(" ")[-1].split(".")[0]  # Extract "Bassett", "Kanaan", etc.
        
        # Load and process the file
        df = pd.read_excel(file)
        df = process_formatting_split(df)  # Handle formatting logic
        
        # Add Player Name column
        df.insert(0, "Player Name", player_name)
        
        dataframes.append(df)
    
    # Combine all processed files into one DataFrame
    combined_df = pd.concat(dataframes, ignore_index=True)
    return combined_df
    