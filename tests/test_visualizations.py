import pandas as pd
import pytest
import plotly.graph_objects as go
from modules.visualizations import create_radar_chart

def test_create_radar_chart_structure():
    """Verify that the radar chart is generated with the correct traces."""
    df = pd.DataFrame({
        "Player Name": ["Player A", "Player B"],
        "Goals": [1.0, 0.5],
        "Assists": [0.2, 0.8]
    })
    selected_players = ["Player A", "Player B"]
    metrics = ["Goals", "Assists"]
    
    fig = create_radar_chart(df, selected_players, metrics)
    
    # 1. Check object type
    assert isinstance(fig, go.Figure)
    
    # 2. Check number of traces (one for each player)
    assert len(fig.data) == 2
    assert fig.data[0].name == "Player A"
    assert fig.data[1].name == "Player B"
    
    # 3. Check labels (theta)
    # Plotly radar charts use 'theta' for the category labels
    assert list(fig.data[0].theta) == metrics

def test_create_radar_chart_normalization():
    """Verify that the data inside the radar chart is normalized 0-1."""
    df = pd.DataFrame({
        "Player Name": ["Best", "Worst"],
        "Goals": [10.0, 0.0]
    })
    selected_players = ["Best", "Worst"]
    metrics = ["Goals"]
    
    fig = create_radar_chart(df, selected_players, metrics)
    
    # Trace 0 is 'Best'
    # Plotly stores values in the 'r' attribute for polar charts
    assert fig.data[0].r[0] == 1.0  # Best should be normalized to 1
    
    # Trace 1 is 'Worst'
    assert fig.data[1].r[0] == 0.0  # Worst should be normalized to 0

def test_create_radar_chart_no_variance():
    """Verify handling when all players have the same stat value."""
    df = pd.DataFrame({
        "Player Name": ["A", "B"],
        "Goals": [90, 90]
    })
    
    fig = create_radar_chart(df, ["A", "B"], ["Goals"])
    
    # If everyone is the same, normalization logic should set everyone to 0
    # (or whatever default you defined in visualizations.py)
    assert fig.data[0].r[0] == 0
    assert fig.data[1].r[0] == 0