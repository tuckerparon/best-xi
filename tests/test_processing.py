import pandas as pd
import pytest
from modules.processing import get_available_positions, filter_players_by_position, aggregate_player_stats

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