def calculate_position_scores(df, metrics_weights):
    """
    Calculate position scores for players based on selected metrics and weights.
    
    The scoring system works as follows:
    1. All metrics are normalized to a 0-1 scale relative to the best performer in each metric
    2. Each metric is weighted according to user input (1-10)
    3. The final score is calculated as: sum(normalized_metric * weight) / sum(weights)
    4. The resulting score will be between 0-10, where:
       - 10 represents the best possible performance across all weighted metrics
       - 0 represents the worst performance across all weighted metrics
       - Scores are relative to the players being compared
    
    Args:
        df (pd.DataFrame): DataFrame containing player metrics
        metrics_weights (dict): Dictionary of metric names and their weights (1-10)
    
    Returns:
        pd.DataFrame: DataFrame with added 'Position Score' column
    """
    # Normalize each metric to 0-1 scale
    for metric in metrics_weights.keys():
        if metric in df.columns:
            min_val = df[metric].min()
            max_val = df[metric].max()
            if max_val > min_val:  # Avoid division by zero
                df[f'{metric}_normalized'] = (df[metric] - min_val) / (max_val - min_val)
            else:
                df[f'{metric}_normalized'] = 0
    
    # Calculate weighted score
    total_weight = sum(metrics_weights.values())
    df['Position Score'] = df.apply(
        lambda row: sum(row[f'{metric}_normalized'] * weight 
                       for metric, weight in metrics_weights.items() 
                       if metric in df.columns) / total_weight * 10,
        axis=1
    )
    
    # Clean up temporary normalized columns
    for metric in metrics_weights.keys():
        if f'{metric}_normalized' in df.columns:
            df = df.drop(columns=[f'{metric}_normalized'])
    
    return df
