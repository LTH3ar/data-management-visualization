"""
STEP 1: DATA INSPECTION
Check all 3 datasets to see what cleaning is needed
"""

import pandas as pd
import numpy as np

print("=" * 70)
print("DATA INSPECTION REPORT")
print("=" * 70)

# ============================================
# DATASET 1: PIMA INDIANS DIABETES
# ============================================
print("\n" + "=" * 70)
print("DATASET 1: PIMA INDIANS DIABETES")
print("=" * 70)

try:
    pima = pd.read_csv('data/pima_diabetes.csv')
    
    print(f"\n✓ Loaded successfully!")
    print(f"  Shape: {pima.shape[0]} rows × {pima.shape[1]} columns")
    print(f"\n  Columns: {list(pima.columns)}")
    
    print("\n📊 BASIC INFO:")
    print(pima.info())
    
    print("\n📈 STATISTICAL SUMMARY:")
    print(pima.describe())
    
    print("\n⚠️  MISSING/ZERO VALUES CHECK:")
    print("Zeros found in each column:")
    for col in pima.columns:
        zero_count = (pima[col] == 0).sum()
        zero_pct = (zero_count / len(pima)) * 100
        if zero_count > 0:
            print(f"  {col}: {zero_count} zeros ({zero_pct:.1f}%)")
    
    print("\n🔍 ISSUES FOUND:")
    print("  ⚠️  Zero values in biological measurements (impossible!)")
    print("     - Glucose = 0 is medically impossible")
    print("     - BloodPressure = 0 is impossible")
    print("     - BMI = 0 is impossible")
    print("  ➜ THESE ZEROS = MISSING VALUES, need to handle!")
    
    print("\n💡 CLEANING NEEDED:")
    print("  1. Replace 0s with NaN for: Glucose, BloodPressure, SkinThickness, Insulin, BMI")
    print("  2. Decide: Drop rows with missing OR impute values")
    
except Exception as e:
    print(f"✗ ERROR: {e}")
    print("  Make sure 'pima_diabetes.csv' is in the same folder!")

# ============================================
# DATASET 2: CDC HEALTH INDICATORS
# ============================================
print("\n" + "=" * 70)
print("DATASET 2: CDC HEALTH INDICATORS")
print("=" * 70)

try:
    cdc = pd.read_csv('data/diabetes_binary_health_indicators_BRFSS2015.csv')
    
    print(f"\n✓ Loaded successfully!")
    print(f"  Shape: {cdc.shape[0]} rows × {cdc.shape[1]} columns")
    print(f"  SIZE: {cdc.shape[0]:,} records - VERY LARGE!")
    
    print(f"\n  Columns ({len(cdc.columns)} total):")
    for i, col in enumerate(cdc.columns, 1):
        print(f"    {i}. {col}")
    
    print("\n📊 FIRST FEW ROWS:")
    print(cdc.head())
    
    print("\n⚠️  MISSING VALUES:")
    missing = cdc.isnull().sum()
    if missing.sum() == 0:
        print("  ✓ NO missing values found!")
    else:
        print(missing[missing > 0])
    
    print("\n📈 DIABETES DISTRIBUTION:")
    print(cdc['Diabetes_binary'].value_counts())
    diabetes_pct = (cdc['Diabetes_binary'].sum() / len(cdc)) * 100
    print(f"  Diabetes rate: {diabetes_pct:.2f}%")
    
    print("\n🔍 ISSUES FOUND:")
    print("  ⚠️  HUGE dataset - may be slow to process")
    print("  ➜ Might need to sample for faster analysis")
    
    print("\n💡 CLEANING NEEDED:")
    print("  1. Check if balanced dataset or needs sampling")
    print("  2. Verify all values are in expected ranges")
    print("  3. Consider creating a smaller subset for testing")
    
except Exception as e:
    print(f"✗ ERROR: {e}")
    print("  Make sure 'diabetes_binary_health_indicators_BRFSS2015.csv' is in the same folder!")

# ============================================
# DATASET 3: WORLD DIABETES PREVALENCE
# ============================================
print("\n" + "=" * 70)
print("DATASET 3: WORLD DIABETES PREVALENCE")
print("=" * 70)

try:
    world = pd.read_csv('data/world_diabetes.csv')
    
    print(f"\n✓ Loaded successfully!")
    print(f"  Shape: {world.shape[0]} rows × {world.shape[1]} columns")
    
    print(f"\n  Columns: {list(world.columns)}")
    
    print("\n📊 FIRST FEW ROWS:")
    print(world.head(10))
    
    print("\n📈 BASIC INFO:")
    print(world.info())
    
    print("\n⚠️  MISSING VALUES:")
    missing = world.isnull().sum()
    if missing.sum() > 0:
        print(missing[missing > 0])
        print(f"\n  Total missing: {missing.sum()} values")
    else:
        print("  ✓ NO missing values!")
    
    # Check year range
    if 'Year' in world.columns:
        print(f"\n📅 YEAR RANGE:")
        print(f"  From: {world['Year'].min()} to {world['Year'].max()}")
        print(f"  Years available: {sorted(world['Year'].unique())}")
    
    # Check countries
    if 'Entity' in world.columns or 'Country' in world.columns:
        country_col = 'Entity' if 'Entity' in world.columns else 'Country'
        print(f"\n🌍 COUNTRIES:")
        print(f"  Total: {world[country_col].nunique()} countries/regions")
        print(f"  Examples: {list(world[country_col].unique()[:10])}")
    
    print("\n🔍 ISSUES FOUND:")
    if missing.sum() > 0:
        print("  ⚠️  Some missing prevalence data")
    print("  ⚠️  May contain non-country entities (regions, income groups)")
    
    print("\n💡 CLEANING NEEDED:")
    print("  1. Remove non-country rows (World, regions, etc.)")
    print("  2. Handle missing values")
    print("  3. Filter to relevant years (e.g., 2000-2022)")
    print("  4. Select key countries for comparison")
    
except Exception as e:
    print(f"✗ ERROR: {e}")
    print("  Make sure 'world_diabetes.csv' is in the same folder!")

# ============================================
# SUMMARY & NEXT STEPS
# ============================================
print("\n" + "=" * 70)
print("SUMMARY: WHAT NEEDS CLEANING")
print("=" * 70)

print("\n📋 CLEANING PRIORITY:")
print("\n1. PIMA DATASET: ⚠️⚠️⚠️ HIGH PRIORITY")
print("   - Replace biological zeros with NaN")
print("   - Handle missing values (impute or drop)")
print("   - This is CRITICAL for accurate analysis!")

print("\n2. CDC DATASET: ⚠️ LOW PRIORITY")
print("   - Already clean!")
print("   - May need sampling if too slow")
print("   - Just verify data ranges")

print("\n3. WORLD DATASET: ⚠️⚠️ MEDIUM PRIORITY")
print("   - Filter out regional aggregates")
print("   - Handle missing values")
print("   - Select recent years")

print("\n" + "=" * 70)
print("✅ INSPECTION COMPLETE!")
print("Next: Run '02_clean_data.py' to clean all datasets")
print("=" * 70)