#!/usr/bin/env python3
"""
CSV Column Dropper Script
Removes specified columns from a CSV file.

Usage:
    python drop_columns.py column1,column2,column3 filename.csv
    
Example:
    python drop_columns.py Code,Year diabetes.csv
    python drop_columns.py "Column Name" data.csv
"""

import sys
import pandas as pd
import os


def drop_columns(columns_to_drop, filename):
    """
    Drop specified columns from a CSV file.
    
    Args:
        columns_to_drop: Comma-separated list of column names to drop
        filename: Path to the CSV file
    """
    try:
        # Read the CSV file
        df = pd.read_csv(filename)
        
        # Parse column names (split by comma and strip whitespace)
        columns_list = [col.strip() for col in columns_to_drop.split(',')]
        
        # Check which columns exist
        existing_columns = []
        missing_columns = []
        
        for col in columns_list:
            if col in df.columns:
                existing_columns.append(col)
            else:
                missing_columns.append(col)
        
        # Warn about missing columns
        if missing_columns:
            print(f"Warning: The following columns were not found and will be skipped:")
            for col in missing_columns:
                print(f"  - {col}")
            print()
        
        # Check if there are any columns to drop
        if not existing_columns:
            print("Error: None of the specified columns exist in the CSV file.")
            print(f"Available columns: {', '.join(df.columns)}")
            sys.exit(1)
        
        # Count columns before dropping
        original_cols = len(df.columns)
        
        # Drop the columns
        df_dropped = df.drop(columns=existing_columns)
        
        # Count columns after dropping
        remaining_cols = len(df_dropped.columns)
        dropped_count = original_cols - remaining_cols
        
        # Check if any columns remain
        if remaining_cols == 0:
            print("Error: Dropping these columns would result in an empty dataset.")
            sys.exit(1)
        
        # Generate output filename
        base_name = os.path.splitext(filename)[0]
        output_filename = f"{base_name}_dropped.csv"
        
        # Save data without dropped columns
        df_dropped.to_csv(output_filename, index=False)
        
        # Print summary
        print(f"Columns dropped: {', '.join(existing_columns)}")
        print(f"Original columns: {original_cols}")
        print(f"Remaining columns: {remaining_cols}")
        print(f"Remaining column names: {', '.join(df_dropped.columns)}")
        print(f"\nFile saved as: {output_filename}")
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


def main():
    # Check command line arguments
    if len(sys.argv) != 3:
        print("Usage: python drop_columns.py column1,column2,column3 filename.csv")
        print("\nExamples:")
        print("  python drop_columns.py Code data.csv")
        print("  python drop_columns.py Code,Year data.csv")
        print('  python drop_columns.py "Column Name,Another Column" data.csv')
        print("\nNote: Use commas to separate multiple column names.")
        sys.exit(1)
    
    columns_to_drop = sys.argv[1]
    filename = sys.argv[2]
    
    drop_columns(columns_to_drop, filename)


if __name__ == "__main__":
    main()