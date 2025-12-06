#!/usr/bin/env python3
"""
Data Cleaning Script for Diabetes Health Indicators Dataset (BRFSS 2015)
Dataset: diabetes_binary_health_indicators_BRFSS2015.csv
Purpose: Clean and prepare data for Diabetes Risk Factors Analysis
"""

import pandas as pd
import numpy as np
import sys
import os
from datetime import datetime


class DiabetesDataCleaner:
    """Class to handle cleaning of diabetes health indicators dataset"""
    
    def __init__(self, input_file):
        self.input_file = input_file
        self.df = None
        self.original_shape = None
        self.cleaning_report = []
        
    def load_data(self):
        """Load the dataset and store original shape"""
        print(f"Loading data from: {self.input_file}")
        try:
            self.df = pd.read_csv(self.input_file)
            self.original_shape = self.df.shape
            print(f"✓ Data loaded successfully: {self.original_shape[0]} rows, {self.original_shape[1]} columns")
            self.cleaning_report.append(f"Original dataset: {self.original_shape[0]} rows × {self.original_shape[1]} columns")
            return True
        except FileNotFoundError:
            print(f"✗ Error: File '{self.input_file}' not found")
            return False
        except Exception as e:
            print(f"✗ Error loading file: {e}")
            return False
    
    def check_data_quality(self):
        """Perform initial data quality checks"""
        print("\n" + "="*60)
        print("DATA QUALITY ASSESSMENT")
        print("="*60)
        
        # Check for missing values
        missing_values = self.df.isnull().sum()
        total_missing = missing_values.sum()
        
        print(f"\n1. Missing Values: {total_missing}")
        if total_missing > 0:
            print("\nColumns with missing values:")
            print(missing_values[missing_values > 0])
            self.cleaning_report.append(f"Missing values found: {total_missing}")
        else:
            print("   ✓ No missing values detected")
            self.cleaning_report.append("No missing values")
        
        # Check for duplicates
        duplicates = self.df.duplicated().sum()
        print(f"\n2. Duplicate Rows: {duplicates}")
        if duplicates > 0:
            print(f"   ⚠ {duplicates} duplicate rows found ({duplicates/len(self.df)*100:.2f}%)")
            self.cleaning_report.append(f"Duplicates found: {duplicates} rows ({duplicates/len(self.df)*100:.2f}%)")
        else:
            print("   ✓ No duplicates detected")
            self.cleaning_report.append("No duplicates")
        
        # Check data types
        print(f"\n3. Data Types:")
        print(self.df.dtypes.value_counts())
        
        # Check for expected columns (based on BRFSS 2015 dataset)
        expected_columns = [
            'Diabetes_binary', 'HighBP', 'HighChol', 'CholCheck', 'BMI', 
            'Smoker', 'Stroke', 'HeartDiseaseorAttack', 'PhysActivity', 
            'Fruits', 'Veggies', 'HvyAlcoholConsump', 'AnyHealthcare', 
            'NoDocbcCost', 'GenHlth', 'MentHlth', 'PhysHlth', 'DiffWalk', 
            'Sex', 'Age', 'Education', 'Income'
        ]
        
        actual_columns = set(self.df.columns)
        expected_set = set(expected_columns)
        
        if actual_columns == expected_set:
            print(f"\n4. Column Names: ✓ All {len(expected_columns)} expected columns present")
        else:
            missing_cols = expected_set - actual_columns
            extra_cols = actual_columns - expected_set
            if missing_cols:
                print(f"   ⚠ Missing columns: {missing_cols}")
            if extra_cols:
                print(f"   ⚠ Extra columns: {extra_cols}")
        
        # Check value ranges for key variables
        print(f"\n5. Value Range Checks:")
        
        # Binary variables (should be 0 or 1)
        binary_vars = ['Diabetes_binary', 'HighBP', 'HighChol', 'CholCheck', 
                       'Smoker', 'Stroke', 'HeartDiseaseorAttack', 'PhysActivity',
                       'Fruits', 'Veggies', 'HvyAlcoholConsump', 'AnyHealthcare',
                       'NoDocbcCost', 'DiffWalk', 'Sex']
        
        invalid_binary = []
        for var in binary_vars:
            if var in self.df.columns:
                unique_vals = self.df[var].unique()
                if not set(unique_vals).issubset({0, 1, 0.0, 1.0}):
                    invalid_binary.append((var, unique_vals))
        
        if invalid_binary:
            print("   ⚠ Variables with unexpected values:")
            for var, vals in invalid_binary:
                print(f"     - {var}: {vals}")
            self.cleaning_report.append(f"Invalid binary values in {len(invalid_binary)} variables")
        else:
            print("   ✓ All binary variables have valid values (0/1)")
        
        # BMI check (reasonable range: 12-70)
        # if 'BMI' in self.df.columns:
        #     bmi_min, bmi_max = self.df['BMI'].min(), self.df['BMI'].max()
        #     print(f"\n   BMI range: {bmi_min} - {bmi_max}")
        #     outlier_bmi = ((self.df['BMI'] < 12) | (self.df['BMI'] > 70)).sum()
        #     if outlier_bmi > 0:
        #         print(f"   ⚠ {outlier_bmi} BMI outliers (<12 or >70)")
        #         self.cleaning_report.append(f"BMI outliers: {outlier_bmi}")
        
        # Mental and Physical Health (should be 0-30)
        for var in ['MentHlth', 'PhysHlth']:
            if var in self.df.columns:
                invalid = ((self.df[var] < 0) | (self.df[var] > 30)).sum()
                if invalid > 0:
                    print(f"   ⚠ {var}: {invalid} values outside range 0-30")
        
        return True
    
    def remove_duplicates(self):
        """Remove duplicate rows"""
        initial_rows = len(self.df)
        self.df = self.df.drop_duplicates()
        removed = initial_rows - len(self.df)
        
        if removed > 0:
            print(f"\n✓ Removed {removed} duplicate rows")
            self.cleaning_report.append(f"Removed duplicates: {removed} rows")
        
        return removed
    
    def handle_missing_values(self):
        """Handle missing values (if any)"""
        missing_count = self.df.isnull().sum().sum()
        
        if missing_count > 0:
            print(f"\n⚠ Handling {missing_count} missing values...")
            
            # For this dataset, we typically drop rows with missing values
            # since the dataset is large and missing values are rare
            initial_rows = len(self.df)
            self.df = self.df.dropna()
            removed = initial_rows - len(self.df)
            
            print(f"✓ Removed {removed} rows with missing values")
            self.cleaning_report.append(f"Removed rows with missing values: {removed}")
        else:
            print("\n✓ No missing values to handle")
        
        return missing_count
    
    def validate_and_clean_ranges(self):
        """Validate and clean value ranges"""
        print("\n" + "="*60)
        print("VALIDATING AND CLEANING VALUE RANGES")
        print("="*60)
        
        initial_rows = len(self.df)
        
        # # Clean BMI outliers (keep reasonable range: 12-70)
        # if 'BMI' in self.df.columns:
        #     bmi_outliers = ((self.df['BMI'] < 12) | (self.df['BMI'] > 70)).sum()
        #     if bmi_outliers > 0:
        #         print(f"\n⚠ Removing {bmi_outliers} rows with BMI outliers (<12 or >70)")
        #         self.df = self.df[(self.df['BMI'] >= 12) & (self.df['BMI'] <= 70)]
        #         self.cleaning_report.append(f"Removed BMI outliers: {bmi_outliers} rows")
        
        # Validate Mental and Physical Health days (0-30)
        for var in ['MentHlth', 'PhysHlth']:
            if var in self.df.columns:
                before = len(self.df)
                self.df = self.df[(self.df[var] >= 0) & (self.df[var] <= 30)]
                removed = before - len(self.df)
                if removed > 0:
                    print(f"⚠ Removed {removed} rows with invalid {var} values")
                    self.cleaning_report.append(f"Removed invalid {var}: {removed} rows")
        
        # Validate GenHlth (should be 1-5)
        if 'GenHlth' in self.df.columns:
            before = len(self.df)
            self.df = self.df[(self.df['GenHlth'] >= 1) & (self.df['GenHlth'] <= 5)]
            removed = before - len(self.df)
            if removed > 0:
                print(f"⚠ Removed {removed} rows with invalid GenHlth values")
                self.cleaning_report.append(f"Removed invalid GenHlth: {removed} rows")
        
        total_removed = initial_rows - len(self.df)
        if total_removed > 0:
            print(f"\n✓ Total rows removed due to invalid ranges: {total_removed}")
        else:
            print("\n✓ All values within valid ranges")
        
        return total_removed
    
    def ensure_correct_dtypes(self):
        """Ensure all columns have correct data types"""
        print("\n" + "="*60)
        print("STANDARDIZING DATA TYPES")
        print("="*60)
        
        # Convert binary variables to integers
        binary_vars = ['Diabetes_binary', 'HighBP', 'HighChol', 'CholCheck', 
                       'Smoker', 'Stroke', 'HeartDiseaseorAttack', 'PhysActivity',
                       'Fruits', 'Veggies', 'HvyAlcoholConsump', 'AnyHealthcare',
                       'NoDocbcCost', 'DiffWalk', 'Sex']
        
        for var in binary_vars:
            if var in self.df.columns:
                self.df[var] = self.df[var].astype(int)
        
        # Convert categorical ordinal variables to integers
        ordinal_vars = ['GenHlth', 'Age', 'Education', 'Income']
        for var in ordinal_vars:
            if var in self.df.columns:
                self.df[var] = self.df[var].astype(int)
        
        # Ensure BMI is float
        if 'BMI' in self.df.columns:
            self.df['BMI'] = self.df['BMI'].astype(float)
        
        # Ensure health days are integers
        for var in ['MentHlth', 'PhysHlth']:
            if var in self.df.columns:
                self.df[var] = self.df[var].astype(int)
        
        print("✓ Data types standardized")
        self.cleaning_report.append("Data types standardized")
        
        return True
    
    def generate_summary_stats(self):
        """Generate summary statistics"""
        print("\n" + "="*60)
        print("SUMMARY STATISTICS")
        print("="*60)
        
        print(f"\nFinal dataset shape: {self.df.shape[0]} rows × {self.df.shape[1]} columns")
        
        # Class distribution
        if 'Diabetes_binary' in self.df.columns:
            diabetes_dist = self.df['Diabetes_binary'].value_counts()
            print(f"\nDiabetes Distribution:")
            print(f"  No Diabetes (0): {diabetes_dist.get(0, 0)} ({diabetes_dist.get(0, 0)/len(self.df)*100:.2f}%)")
            print(f"  Diabetes (1):    {diabetes_dist.get(1, 0)} ({diabetes_dist.get(1, 0)/len(self.df)*100:.2f}%)")
        
        # Numeric variables summary
        print(f"\nNumeric Variables Summary:")
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        print(self.df[numeric_cols].describe())
        
        return True
    
    def save_cleaned_data(self, output_file=None):
        """Save the cleaned dataset"""
        if output_file is None:
            base_name = os.path.splitext(self.input_file)[0]
            output_file = f"{base_name}_cleaned.csv"
        
        print(f"\n{'='*60}")
        print("SAVING CLEANED DATA")
        print("="*60)
        
        try:
            self.df.to_csv(output_file, index=False)
            print(f"✓ Cleaned data saved to: {output_file}")
            self.cleaning_report.append(f"Saved to: {output_file}")
            return output_file
        except Exception as e:
            print(f"✗ Error saving file: {e}")
            return None
    
    def generate_report(self, report_file=None):
        """Generate a cleaning report"""
        if report_file is None:
            base_name = os.path.splitext(self.input_file)[0]
            report_file = f"{base_name}_cleaning_report.txt"
        
        print(f"\n{'='*60}")
        print("GENERATING CLEANING REPORT")
        print("="*60)
        
        with open(report_file, 'w') as f:
            f.write("="*60 + "\n")
            f.write("DATA CLEANING REPORT\n")
            f.write("Diabetes Health Indicators Dataset (BRFSS 2015)\n")
            f.write("="*60 + "\n\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Input File: {self.input_file}\n\n")
            
            f.write("CLEANING STEPS:\n")
            f.write("-"*60 + "\n")
            for i, step in enumerate(self.cleaning_report, 1):
                f.write(f"{i}. {step}\n")
            
            f.write("\n" + "="*60 + "\n")
            f.write("FINAL DATASET SUMMARY\n")
            f.write("="*60 + "\n")
            f.write(f"Final shape: {self.df.shape[0]} rows × {self.df.shape[1]} columns\n")
            f.write(f"Rows removed: {self.original_shape[0] - self.df.shape[0]}\n")
            f.write(f"Data reduction: {(self.original_shape[0] - self.df.shape[0])/self.original_shape[0]*100:.2f}%\n\n")
            
            if 'Diabetes_binary' in self.df.columns:
                diabetes_dist = self.df['Diabetes_binary'].value_counts()
                f.write("Diabetes Distribution:\n")
                f.write(f"  No Diabetes (0): {diabetes_dist.get(0, 0)} ({diabetes_dist.get(0, 0)/len(self.df)*100:.2f}%)\n")
                f.write(f"  Diabetes (1):    {diabetes_dist.get(1, 0)} ({diabetes_dist.get(1, 0)/len(self.df)*100:.2f}%)\n")
        
        print(f"✓ Cleaning report saved to: {report_file}")
        return report_file
    
    def run_complete_cleaning(self):
        """Run the complete cleaning pipeline"""
        print("\n" + "="*60)
        print("DIABETES HEALTH INDICATORS DATA CLEANING")
        print("="*60 + "\n")
        
        # Load data
        if not self.load_data():
            return False
        
        # Check data quality
        self.check_data_quality()
        
        # Clean data
        print("\n" + "="*60)
        print("CLEANING DATA")
        print("="*60)
        
        self.remove_duplicates()
        self.handle_missing_values()
        self.validate_and_clean_ranges()
        self.ensure_correct_dtypes()
        
        # Generate summary
        self.generate_summary_stats()
        
        # Save results
        output_file = self.save_cleaned_data()
        report_file = self.generate_report()
        
        print("\n" + "="*60)
        print("CLEANING COMPLETE!")
        print("="*60)
        print(f"\nOriginal: {self.original_shape[0]} rows")
        print(f"Cleaned:  {self.df.shape[0]} rows")
        print(f"Removed:  {self.original_shape[0] - self.df.shape[0]} rows ({(self.original_shape[0] - self.df.shape[0])/self.original_shape[0]*100:.2f}%)")
        print(f"\nOutput files:")
        print(f"  - {output_file}")
        print(f"  - {report_file}")
        
        return True


def main():
    """Main function to run the cleaning script"""
    if len(sys.argv) != 2:
        print("Usage: python cleaning.py <input_csv_file>")
        print("Example: python cleaning.py diabetes_binary_health_indicators_BRFSS2015.csv")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # Create cleaner instance and run
    cleaner = DiabetesDataCleaner(input_file)
    success = cleaner.run_complete_cleaning()
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()