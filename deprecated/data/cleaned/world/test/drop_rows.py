#!/usr/bin/env python3
"""
CSV Row Dropper Script
Removes rows with empty cells in a specified column from a CSV file.

Usage:
    python drop_empty_rows.py selected_column filename.csv
"""

import sys
import pandas as pd
import os


def drop_empty_rows(column_name, filename):
    """
    Remove rows with empty cells in the specified column.
    
    Args:
        column_name: Name of the column to check for empty values
        filename: Path to the CSV file
    """
    try:
        # Read the CSV file
        df = pd.read_csv(filename)
        
        # Check if column exists
        if column_name not in df.columns:
            print(f"Error: Column '{column_name}' not found in the CSV file.")
            print(f"Available columns: {', '.join(df.columns)}")
            sys.exit(1)
        
        # Count rows before cleaning
        original_rows = len(df)
        
        # Remove rows where the specified column is empty (NaN, None, or empty string)
        df_cleaned = df.dropna(subset=[column_name])
        df_cleaned = df_cleaned[df_cleaned[column_name].astype(str).str.strip() != '']
        
        # Count rows after cleaning
        cleaned_rows = len(df_cleaned)
        removed_rows = original_rows - cleaned_rows
        
        # Generate output filename
        base_name = os.path.splitext(filename)[0]
        output_filename = f"{base_name}_dropped_rows.csv"
        
        # Save cleaned data
        df_cleaned.to_csv(output_filename, index=False)
        
        # Print summary
        print(f"Column checked: '{column_name}'")
        print(f"Original rows: {original_rows}")
        print(f"Rows removed: {removed_rows}")
        print(f"Remaining rows: {cleaned_rows}")
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
        print("Usage: python drop_empty_rows.py selected_column filename.csv")
        print("\nExample:")
        print("  python drop_empty_rows.py Entity diabetes.csv")
        print("  python drop_empty_rows.py Code data.csv")
        sys.exit(1)
    
    column_name = sys.argv[1]
    filename = sys.argv[2]
    
    drop_empty_rows(column_name, filename)


if __name__ == "__main__":
    main()