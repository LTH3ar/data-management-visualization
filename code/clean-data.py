"""
STEP 2: DATA CLEANING
Clean all 3 datasets and save cleaned versions
"""

import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer

print("=" * 70)
print("DATA CLEANING PROCESS")
print("=" * 70)

# ============================================
# DATASET 1: PIMA INDIANS DIABETES - CRITICAL CLEANING
# ============================================
print("\n" + "=" * 70)
print("CLEANING DATASET 1: PIMA INDIANS DIABETES")
print("=" * 70)

try:
    pima = pd.read_csv('data/pima_diabetes.csv')
    print(f"✓ Loaded: {pima.shape[0]} rows × {pima.shape[1]} columns")
    
    # Show original zeros
    print("\n⚠️  BEFORE CLEANING - Impossible zeros:")
    cols_with_zeros = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
    for col in cols_with_zeros:
        zero_count = (pima[col] == 0).sum()
        print(f"  {col}: {zero_count} zeros")
    
    # Step 1: Replace zeros with NaN for biological measurements
    print("\n🔧 Step 1: Replacing impossible zeros with NaN...")
    pima_clean = pima.copy()
    for col in cols_with_zeros:
        pima_clean[col] = pima_clean[col].replace(0, np.nan)
    
    # Show missing values
    print("\n📊 Missing values after replacement:")
    missing_counts = pima_clean.isnull().sum()
    for col in cols_with_zeros:
        if missing_counts[col] > 0:
            pct = (missing_counts[col] / len(pima_clean)) * 100
            print(f"  {col}: {missing_counts[col]} ({pct:.1f}%)")
    
    # Step 2: Option A - Drop rows with any missing values
    print("\n🔧 Step 2A: Creating dataset WITHOUT missing values (drop rows)...")
    pima_complete = pima_clean.dropna()
    print(f"  Original: {len(pima_clean)} rows")
    print(f"  After dropping: {len(pima_complete)} rows")
    print(f"  Lost: {len(pima_clean) - len(pima_complete)} rows ({(len(pima_clean) - len(pima_complete))/len(pima_clean)*100:.1f}%)")
    
    # Step 3: Option B - Impute missing values with median
    print("\n🔧 Step 2B: Creating dataset WITH imputed values (median strategy)...")
    pima_imputed = pima_clean.copy()
    
    for col in cols_with_zeros:
        if pima_imputed[col].isnull().sum() > 0:
            median_value = pima_imputed[col].median()
            pima_imputed[col].fillna(median_value, inplace=True)
            print(f"  {col}: filled with median = {median_value:.1f}")
    
    # Save both versions
    pima_complete.to_csv('pima_diabetes_clean.csv', index=False)
    pima_imputed.to_csv('pima_diabetes_imputed.csv', index=False)
    
    print("\n✅ SAVED:")
    print(f"  1. 'pima_diabetes_clean.csv' - {len(pima_complete)} rows (dropped missing)")
    print(f"  2. 'pima_diabetes_imputed.csv' - {len(pima_imputed)} rows (imputed missing)")
    print("\n💡 Recommendation: Use 'pima_diabetes_imputed.csv' to keep more data!")
    
    # Verify no more zeros
    print("\n✓ Verification - Zeros in cleaned data:")
    for col in cols_with_zeros:
        zero_count = (pima_imputed[col] == 0).sum()
        print(f"  {col}: {zero_count} zeros (should be 0)")
    
except Exception as e:
    print(f"✗ ERROR: {e}")

# ============================================
# DATASET 2: CDC HEALTH INDICATORS - MINIMAL CLEANING
# ============================================
print("\n" + "=" * 70)
print("CLEANING DATASET 2: CDC HEALTH INDICATORS")
print("=" * 70)

try:
    cdc = pd.read_csv('data/diabetes_binary_health_indicators_BRFSS2015.csv')
    print(f"✓ Loaded: {cdc.shape[0]:,} rows × {cdc.shape[1]} columns")
    
    # Check for missing values
    missing = cdc.isnull().sum().sum()
    print(f"\n📊 Missing values: {missing}")
    
    if missing == 0:
        print("✓ Dataset is already clean - no missing values!")
    
    # Check data ranges
    print("\n🔧 Verifying data ranges...")
    print(f"  Diabetes_binary: {sorted(cdc['Diabetes_binary'].unique())}")
    
    # Optional: Create a smaller sample for faster testing
    print("\n🔧 Creating smaller sample for faster analysis...")
    
    # Stratified sample to maintain diabetes ratio
    diabetes_yes = cdc[cdc['Diabetes_binary'] == 1].sample(n=5000, random_state=42)
    diabetes_no = cdc[cdc['Diabetes_binary'] == 0].sample(n=5000, random_state=42)
    cdc_sample = pd.concat([diabetes_yes, diabetes_no]).sample(frac=1, random_state=42)
    
    print(f"  Full dataset: {len(cdc):,} rows")
    print(f"  Sample: {len(cdc_sample):,} rows (balanced)")
    
    # Save
    cdc.to_csv('cdc_diabetes_clean.csv', index=False)
    cdc_sample.to_csv('cdc_diabetes_sample.csv', index=False)
    
    print("\n✅ SAVED:")
    print(f"  1. 'cdc_diabetes_clean.csv' - Full dataset ({len(cdc):,} rows)")
    print(f"  2. 'cdc_diabetes_sample.csv' - Sample ({len(cdc_sample):,} rows)")
    print("\n💡 Use sample for quick testing, full dataset for final analysis!")
    
except Exception as e:
    print(f"✗ ERROR: {e}")

# ============================================
# DATASET 3: WORLD DIABETES PREVALENCE - MODERATE CLEANING
# ============================================
print("\n" + "=" * 70)
print("CLEANING DATASET 3: WORLD DIABETES PREVALENCE")
print("=" * 70)

try:
    world = pd.read_csv('data/world_diabetes.csv')
    print(f"✓ Loaded: {world.shape[0]} rows × {world.shape[1]} columns")
    
    # Identify column names (they vary by source)
    print(f"\n📋 Columns: {list(world.columns)}")
    
    # Standardize column names
    print("\n🔧 Standardizing column names...")
    
    # Common variations from Our World in Data
    rename_dict = {}
    for col in world.columns:
        if 'entity' in col.lower() or 'country' in col.lower():
            rename_dict[col] = 'Country'
        elif 'year' in col.lower():
            rename_dict[col] = 'Year'
        elif 'code' in col.lower():
            rename_dict[col] = 'Code'
        elif 'diabetes' in col.lower() or 'prevalence' in col.lower():
            rename_dict[col] = 'Diabetes_Prevalence'
    
    world_clean = world.rename(columns=rename_dict)
    print(f"  Renamed columns: {list(world_clean.columns)}")
    
    # Remove regional aggregates (keep only actual countries)
    print("\n🔧 Filtering actual countries only...")
    
    # Regions to exclude (common aggregates)
    exclude_terms = [
        'World', 'Income', 'Africa', 'Asia', 'Europe', 'America', 
        'Region', 'Countries', 'OECD', 'G20', 'Saharan', 'Eastern',
        'Western', 'Northern', 'Southern', 'Central', 'Caribbean',
        'Pacific', 'Arab', 'Small states', 'Fragile', 'IDA', 'IBRD'
    ]
    
    # Filter out aggregates
    if 'Country' in world_clean.columns:
        mask = ~world_clean['Country'].str.contains('|'.join(exclude_terms), case=False, na=False)
        world_clean = world_clean[mask]
        print(f"  Before filtering: {len(world)} rows")
        print(f"  After filtering: {len(world_clean)} rows")
    
    # Filter to recent years only (if Year column exists)
    if 'Year' in world_clean.columns:
        print("\n🔧 Filtering to recent years (2000-2024)...")
        world_clean = world_clean[world_clean['Year'] >= 2000]
        print(f"  Years included: {world_clean['Year'].min()} to {world_clean['Year'].max()}")
    
    # Handle missing prevalence data
    if 'Diabetes_Prevalence' in world_clean.columns:
        print("\n📊 Missing prevalence data:")
        missing_prev = world_clean['Diabetes_Prevalence'].isnull().sum()
        print(f"  Missing values: {missing_prev}")
        
        if missing_prev > 0:
            print("\n🔧 Removing rows with missing prevalence...")
            world_clean = world_clean.dropna(subset=['Diabetes_Prevalence'])
            print(f"  Rows remaining: {len(world_clean)}")
    
    # Save cleaned version
    world_clean.to_csv('world_diabetes_clean.csv', index=False)
    
    print("\n✅ SAVED:")
    print(f"  'world_diabetes_clean.csv' - {len(world_clean)} rows")
    
    # Show some statistics
    if 'Country' in world_clean.columns:
        print(f"\n📊 Countries included: {world_clean['Country'].nunique()}")
        print(f"  Sample countries: {list(world_clean['Country'].unique()[:10])}")
    
    if 'Diabetes_Prevalence' in world_clean.columns:
        print(f"\n📊 Prevalence statistics:")
        print(f"  Mean: {world_clean['Diabetes_Prevalence'].mean():.2f}%")
        print(f"  Min: {world_clean['Diabetes_Prevalence'].min():.2f}%")
        print(f"  Max: {world_clean['Diabetes_Prevalence'].max():.2f}%")
    
except Exception as e:
    print(f"✗ ERROR: {e}")
    print("  Note: Column names may vary. Check the actual column names in your file.")

# ============================================
# FINAL SUMMARY
# ============================================
print("\n" + "=" * 70)
print("CLEANING COMPLETE! 🎉")
print("=" * 70)

print("\n📁 CLEANED FILES CREATED:")
print("\n1. PIMA DATASET:")
print("   ✓ pima_diabetes_clean.csv (dropped missing)")
print("   ✓ pima_diabetes_imputed.csv (imputed missing) ← RECOMMENDED")

print("\n2. CDC DATASET:")
print("   ✓ cdc_diabetes_clean.csv (full dataset)")
print("   ✓ cdc_diabetes_sample.csv (10k sample) ← Use for testing")

print("\n3. WORLD DATASET:")
print("   ✓ world_diabetes_clean.csv (filtered & cleaned)")

print("\n" + "=" * 70)
print("NEXT STEPS:")
print("=" * 70)
print("1. ✅ Data is now ready for analysis!")
print("2. 📊 Next: Run exploratory data analysis (EDA)")
print("3. 📈 Then: Statistical tests and modeling")
print("\nRun '03_exploratory_analysis.py' next!")
print("=" * 70)