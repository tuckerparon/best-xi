from modules.processing import process_formatting_split, load_and_process_files
from modules.scoring import calculate_position_scores
import pandas as pd

if __name__ == "__main__":
    # Load the raw Excel file as a DataFrame
    raw_df = pd.read_excel('Player stats S. Kanaan.xlsx')
    print("Columns BEFORE processing:")
    print(raw_df.columns.tolist())
    print("\nSample data BEFORE processing:")
    print(raw_df.head())

    # Process the DataFrame using your formatting function
    processed_df = process_formatting_split(raw_df.copy())
    print("\nColumns AFTER process_formatting_split:")
    print(processed_df.columns.tolist())
    print("\nSample data AFTER process_formatting_split:")
    print(processed_df.head())

    # Now run through the full load_and_process_files logic for comparison
    with open('Player stats S. Kanaan.xlsx', 'rb') as f:
        df = load_and_process_files([f])
        print("\nColumns AFTER load_and_process_files:")
        print(df.columns.tolist())
        print("\nSample data AFTER load_and_process_files:")
        print(df.head())

    # Test normalization for a negative metric
    test_metrics = {'Fouls': 1, 'Yellow cards': 1, 'Losses (total)': 1}
    scored_df = calculate_position_scores(df.copy(), test_metrics)
    print("\nNormalized values for negative metrics (should be higher for lower raw values):")
    for metric in test_metrics:
        norm_col = f'{metric}_normalized'
        if norm_col in scored_df.columns:
            print(f"{metric}: {scored_df[[metric, norm_col]].head()}") 