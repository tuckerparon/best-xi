import pandas as pd

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
