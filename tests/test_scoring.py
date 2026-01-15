import pandas as pd
import pytest
from modules.scoring import calculate_position_scores

def test_calculate_position_scores_basic():
    """Test standard normalization and weighted scoring on a 0-10 scale."""
    df = pd.DataFrame({
        "Player Name": ["Best", "Average", "Worst"],
        "Goals": [10.0, 5.0, 0.0],
        "Assists": [2.0, 1.0, 0.0]
    })
    
    # Weight Goals heavily (10) and Assists moderately (5)
    weights = {"Goals": 10, "Assists": 5}
    
    result = calculate_position_scores(df.copy(), weights)
    
    # Check that 'Position Score' was added
    assert "Position Score" in result.columns
    
    # Best player should have 10, worst should have 0
    scores = result.set_index("Player Name")["Position Score"]
    assert scores["Best"] == 10.0
    assert scores["Worst"] == 0.0
    assert 0 < scores["Average"] < 10

def test_calculate_position_scores_negative_metrics():
    """Test that metrics in NEGATIVE_METRICS (like Fouls) are correctly inverted."""
    df = pd.DataFrame({
        "Player Name": ["Disciplined", "Aggressive"],
        "Fouls": [0, 10]  # Fouls is a negative metric
    })
    
    weights = {"Fouls": 10}
    
    result = calculate_position_scores(df.copy(), weights)
    scores = result.set_index("Player Name")["Position Score"]
    
    # Lower fouls should result in a higher score
    assert scores["Disciplined"] == 10.0
    assert scores["Aggressive"] == 0.0

def test_calculate_position_scores_no_variance():
    """Test behavior when all players have the same value for a metric."""
    df = pd.DataFrame({
        "Player Name": ["Player A", "Player B"],
        "Minutes Played": [90, 90]
    })
    
    weights = {"Minutes Played": 10}
    
    result = calculate_position_scores(df.copy(), weights)
    
    # Current logic: if max == min, normalized value is 0
    # (0 * weight) / weight * 10 = 0
    assert (result["Position Score"] == 0.0).all()

def test_calculate_position_scores_missing_columns():
    """Test that weights for non-existent columns are handled gracefully."""
    df = pd.DataFrame({
        "Player Name": ["Best", "Worst"],
        "Goals": [1.0, 0.0]  # Variance ensures 'Best' gets 1.0 normalization
    })

    # 'MissingMetric' is not in the DataFrame
    weights = {"Goals": 10, "MissingMetric": 10}

    result = calculate_position_scores(df.copy(), weights)

    # Total weight is 20 (10 + 10). 
    # Best: Goals_norm (1.0) * weight (10) / total_weight (20) * 10 = 5.0
    # Worst: Goals_norm (0.0) * weight (10) / total_weight (20) * 10 = 0.0
    scores = result.set_index("Player Name")["Position Score"]
    assert scores["Best"] == 5.0
    assert scores["Worst"] == 0.0

def test_calculate_position_scores_cleanup():
    """Verify that temporary normalization columns are removed after calculation."""
    df = pd.DataFrame({
        "Player Name": ["A"],
        "Goals": [1]
    })
    
    weights = {"Goals": 10}
    result = calculate_position_scores(df.copy(), weights)
    
    # Ensure temporary columns like 'Goals_normalized' are dropped
    assert "Goals_normalized" not in result.columns