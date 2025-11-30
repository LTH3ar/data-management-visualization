import pandas as pd
import numpy as np

# Load cleaned data
df = pd.read_csv('pima_diabetes_cleaned.csv')

# 1. BMI Categories (WHO standard)
df['BMI_Category'] = pd.cut(df['BMI'], 
                             bins=[0, 18.5, 25, 30, 100],
                             labels=['Underweight', 'Normal', 'Overweight', 'Obese'])

# 2. Age Groups
df['Age_Group'] = pd.cut(df['Age'], 
                          bins=[0, 30, 40, 50, 100],
                          labels=['21-30', '31-40', '41-50', '50+'])

# 3. Glucose Categories (ADA standard)
df['Glucose_Category'] = pd.cut(df['Glucose'],
                                 bins=[0, 100, 125, 300],
                                 labels=['Normal', 'Prediabetes', 'Diabetes'])

# 4. Blood Pressure Categories (AHA standard)
df['BP_Category'] = pd.cut(df['BloodPressure'],
                            bins=[0, 80, 90, 120, 200],
                            labels=['Normal', 'Elevated', 'High', 'Very High'])

# 5. Pregnancy Risk Groups
df['Pregnancy_Group'] = pd.cut(df['Pregnancies'],
                                bins=[-1, 0, 3, 6, 20],
                                labels=['None', 'Low (1-3)', 'Medium (4-6)', 'High (7+)'])

# 6. Risk Score (simple additive - clinical factors)
df['Clinical_Risk_Score'] = (
    (df['BMI'] > 30).astype(int) +           # Obesity
    (df['Glucose'] > 125).astype(int) +      # Prediabetes/Diabetes glucose
    (df['BloodPressure'] > 90).astype(int) + # Hypertension
    (df['Age'] > 35).astype(int)             # Older age
)

# Save with new features
df.to_csv('pima_diabetes_with_features.csv', index=False)
print(f"✓ Saved with {len(df.columns)} columns (added {len(df.columns) - 9} features)")
print(df[['BMI', 'BMI_Category', 'Age', 'Age_Group', 'Clinical_Risk_Score']].head())