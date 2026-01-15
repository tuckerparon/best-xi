import pandas as pd
import pytest
from modules.processing import get_available_positions, filter_players_by_position, aggregate_player_stats, process_formatting_split

def test_get_available_positions():
    # Setup sample data
    df = pd.DataFrame({
        "Position": ["CF, ST", "LW", "GK", None]
    })
    
    positions = get_available_positions(df)
    
    # Check for both individual and grouped positions
    assert "GK" in positions
    assert "LW" in positions
    assert "ST (CF/ST)" in positions  # Grouped name from POSITION_MAP

def test_filter_players_by_position():
    df = pd.DataFrame({
        "Player Name": ["Player A", "Player B", "Player C"],
        "Position": ["CF, ST", "LW", "GK"]
    })
    
    # Test filtering by individual position
    filtered_lw = filter_players_by_position(df, "LW")
    assert len(filtered_lw) == 1
    assert filtered_lw.iloc[0]["Player Name"] == "Player B"
    
    # Test filtering by grouped position
    filtered_st = filter_players_by_position(df, "ST (CF/ST)")
    assert len(filtered_st) == 1
    assert filtered_st.iloc[0]["Player Name"] == "Player A"

def test_aggregate_player_stats():
    df = pd.DataFrame({
        "Player Name": ["Player A", "Player A"],
        "Minutes Played": [90, 45],
        "Goals": [1, 0],
        "Assists": [0, 1]
    })
    
    aggregated, numeric_cols = aggregate_player_stats(df)
    
    player_a = aggregated[aggregated["Player Name"] == "Player A"].iloc[0]
    assert player_a["Minutes Played at Position"] == 135
    assert player_a["Games Played at Position"] == 2
    assert player_a["Goals"] == 0.5  # Mean of 1 and 0

def test_process_formatting_split():
    # Simulate a DataFrame exactly as it comes from Excel with merged headers
    df = pd.DataFrame({
        "Dribbles / successful": [10, 0], # 0 to test division handling
        "Unnamed: 1": [5, 0],            # The 'successful' count
        "Normal Metric": [1, 2],
        "Yellow card": [45, 90]          # Should be dropped
    })
    
    processed = process_formatting_split(df.copy())
    
    # 1. Check splitting logic
    assert "Dribbles (total)" in processed.columns
    assert "Dribbles (successful)" in processed.columns
    assert processed["Dribbles (total)"].iloc[0] == 10
    
    # 2. Check percentage calculation
    # (5 / 10) * 100 = 50.0
    assert processed["% Dribbles (successful)"].iloc[0] == 50.0
    # Handle 0/0 case (should be 0 via .fillna(0))
    assert processed["% Dribbles (successful)"].iloc[1] == 0.0
    
    # 3. Check column cleanup
    assert "Yellow card" not in processed.columns
    assert "Normal Metric" in processed.columns
