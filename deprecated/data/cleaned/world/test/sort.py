#!/usr/bin/env python3
"""
Sort and split diabetes prevalence data by a selected column.

Usage:
    python sort.py <sort_column> <output_dir> [input_file]
    
Arguments:
    sort_column: Column name to group by (e.g., 'Entity', 'Code', 'Year')
    output_dir: Directory to save output files
    input_file: Path to input CSV file (default: diabetes_data.csv)
    
Example:
    python sort.py Entity output_by_country
    python sort.py Year output_by_year
    python sort.py Code output_by_code
"""

import sys
import os
import pandas as pd
from pathlib import Path


def sanitize_filename(name):
    """
    Convert a string into a safe filename.
    
    Args:
        name: String to sanitize
        
    Returns:
        Safe filename string
    """
    # Replace spaces and special characters
    safe_name = str(name).replace(' ', '_').replace('/', '-')
    # Remove or replace other problematic characters
    safe_chars = []
    for char in safe_name:
        if char.isalnum() or char in ['_', '-', '.']:
            safe_chars.append(char)
        else:
            safe_chars.append('_')
    return ''.join(safe_chars)


def sort_and_split_data(input_file, sort_column, output_dir):
    """
    Sort data by column and output separate files for each unique value.
    
    Args:
        input_file: Path to input CSV file
        sort_column: Column name to group by
        output_dir: Directory to save output files
    """
    # Read the data
    print(f"Reading data from: {input_file}")
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    print(f"Loaded {len(df)} rows with columns: {', '.join(df.columns)}")
    
    # Check if sort column exists
    if sort_column not in df.columns:
        print(f"\nError: Column '{sort_column}' not found in data.")
        print(f"Available columns: {', '.join(df.columns)}")
        sys.exit(1)
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    print(f"\nOutput directory: {output_path.absolute()}")
    
    # Get unique values in the sort column
    unique_values = df[sort_column].unique()
    print(f"\nFound {len(unique_values)} unique values in '{sort_column}' column")
    
    # Sort and save data for each unique value
    files_created = []
    for value in sorted(unique_values, key=lambda x: str(x)):
        # Filter data for this value
        filtered_df = df[df[sort_column] == value]
        
        # Sort by all columns for consistent ordering
        # Prioritize Year if it exists
        if 'Year' in filtered_df.columns and sort_column != 'Year':
            filtered_df = filtered_df.sort_values(['Year'] + [col for col in filtered_df.columns if col != 'Year'])
        else:
            filtered_df = filtered_df.sort_values(filtered_df.columns.tolist())
        
        # Create safe filename
        safe_value = sanitize_filename(value)
        output_file = output_path / f"{sort_column}_{safe_value}.csv"
        
        # Save to CSV
        filtered_df.to_csv(output_file, index=False)
        files_created.append((value, len(filtered_df), output_file))
    
    # Print summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total files created: {len(files_created)}")
    print(f"\nSample of created files:")
    for value, count, filepath in files_created[:10]:
        print(f"  - {filepath.name}: {count} rows ({value})")
    
    if len(files_created) > 10:
        print(f"  ... and {len(files_created) - 10} more files")
    
    print(f"\nAll files saved to: {output_path.absolute()}")
    

def main():
    """Main entry point for the script."""
    # Check command line arguments
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    
    sort_column = sys.argv[1]
    output_dir = sys.argv[2]
    input_file = sys.argv[3] if len(sys.argv) > 3 else "diabetes_data.csv"
    
    print("="*80)
    print("DIABETES DATA SORTER")
    print("="*80)
    print(f"Sort column: {sort_column}")
    print(f"Input file: {input_file}")
    print(f"Output directory: {output_dir}")
    print("="*80 + "\n")
    
    sort_and_split_data(input_file, sort_column, output_dir)
    

if __name__ == "__main__":
    main()