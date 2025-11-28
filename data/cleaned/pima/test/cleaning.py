#!/usr/bin/env python3
"""
Simple Pima Dataset Cleaner
Handles physiologically impossible zero values in medical measurements
"""

import pandas as pd
import sys

def clean_pima_dataset(input_file='pima.csv', output_file='pima_cleaned.csv'):
    """
    Clean Pima diabetes dataset by handling impossible zero values
    
    Columns where 0 is impossible:
    - Glucose: Can't survive with 0 glucose
    - BloodPressure: Can't be alive with 0 BP
    - SkinThickness: Everyone has skin
    - Insulin: 0 often indicates missing data
    - BMI: Can't have 0 body mass
    """
    
    # Read the dataset
    print(f"Reading {input_file}...")
    df = pd.read_csv(input_file)
    
    print(f"Original dataset shape: {df.shape}")
    print(f"\nZero value counts by column:")
    
    # Columns where 0 is physiologically impossible
    zero_invalid_cols = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
    
    # Show zero counts
    for col in zero_invalid_cols:
        zero_count = (df[col] == 0).sum()
        print(f"  {col}: {zero_count} zeros ({zero_count/len(df)*100:.1f}%)")
    
    # Replace 0s with NaN for impossible columns
    print(f"\nReplacing zeros with NaN in: {', '.join(zero_invalid_cols)}")
    df[zero_invalid_cols] = df[zero_invalid_cols].replace(0, pd.NA)
    
    # Option 1: Drop rows with any missing values
    df_cleaned = df.dropna()
    
    print(f"\nCleaned dataset shape: {df_cleaned.shape}")
    print(f"Rows removed: {len(df) - len(df_cleaned)} ({(len(df) - len(df_cleaned))/len(df)*100:.1f}%)")
    
    # Save cleaned dataset
    df_cleaned.to_csv(output_file, index=False)
    print(f"\nCleaned dataset saved to: {output_file}")
    
    # Show basic stats
    print(f"\nCleaned dataset summary:")
    print(df_cleaned.describe())
    
    return df_cleaned

if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'pima.csv'
    output_file = 'pima_cleaned.csv'
    
    try:
        clean_pima_dataset(input_file, output_file)
    except FileNotFoundError:
        print(f"Error: {input_file} not found!")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)