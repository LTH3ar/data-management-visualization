#!/usr/bin/env python3
"""
CSV Pivot Script
Transforms data from long format to wide format by pivoting the Year column.
Each unique year becomes a separate column.

Usage:
    python pivot_years.py filename.csv
"""

import sys
import pandas as pd
import os


def pivot_years(filename):
    """
    Pivot the CSV so that each year becomes a separate column.
    
    Args:
        filename: Path to the CSV file
    """
    try:
        # Read the CSV file
        df = pd.read_csv(filename)
        
        # Check if required columns exist
        required_cols = ['Entity', 'Code', 'Year']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            print(f"Error: Missing required columns: {', '.join(missing_cols)}")
            print(f"Available columns: {', '.join(df.columns)}")
            sys.exit(1)
        
        # Get the value column name (the 4th column, assuming it's the data column)
        value_cols = [col for col in df.columns if col not in ['Entity', 'Code', 'Year']]
        
        if not value_cols:
            print("Error: No value column found to pivot.")
            sys.exit(1)
        
        value_col = value_cols[0]
        print(f"Pivoting column: '{value_col}'")
        
        # Pivot the data
        df_pivoted = df.pivot_table(
            index=['Entity', 'Code'],
            columns='Year',
            values=value_col,
            aggfunc='first'  # Use 'first' in case of duplicates
        )
        
        # Reset index to make Entity and Code regular columns
        df_pivoted = df_pivoted.reset_index()
        
        # Rename columns to include original column name for clarity
        df_pivoted.columns.name = None  # Remove the 'Year' label from column index
        year_cols = [col for col in df_pivoted.columns if col not in ['Entity', 'Code']]
        
        # Sort columns: Entity, Code, then years in ascending order
        sorted_cols = ['Entity', 'Code'] + sorted(year_cols)
        df_pivoted = df_pivoted[sorted_cols]
        
        # Generate output filename
        base_name = os.path.splitext(filename)[0]
        output_filename = f"{base_name}_pivoted.csv"
        
        # Save pivoted data
        df_pivoted.to_csv(output_filename, index=False)
        
        # Print summary
        print(f"\nOriginal shape: {df.shape[0]} rows × {df.shape[1]} columns")
        print(f"Pivoted shape: {df_pivoted.shape[0]} rows × {df_pivoted.shape[1]} columns")
        print(f"Years included: {', '.join(map(str, sorted(year_cols)))}")
        print(f"\nPivoted file saved as: {output_filename}")
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


def main():
    # Check command line arguments
    if len(sys.argv) != 2:
        print("Usage: python pivot_years.py filename.csv")
        print("\nExample:")
        print("  python pivot_years.py diabetes_data.csv")
        print("\nThis will transform data from:")
        print("  Entity, Code, Year, Value")
        print("  USA, US, 2011, 10.5")
        print("  USA, US, 2024, 12.3")
        print("\nTo:")
        print("  Entity, Code, 2011, 2024")
        print("  USA, US, 10.5, 12.3")
        sys.exit(1)
    
    filename = sys.argv[1]
    pivot_years(filename)


if __name__ == "__main__":
    main()