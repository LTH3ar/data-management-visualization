import pandas as pd
import numpy as np

# Load cleaned data
df = pd.read_csv('diabetes_binary_health_indicators_BRFSS2015_cleaned.csv')

# 1. BMI Categories
df['BMI_Category'] = pd.cut(df['BMI'], 
                             bins=[0, 18.5, 25, 30, 100],
                             labels=['Underweight', 'Normal', 'Overweight', 'Obese'])

# 2. Age Groups (BRFSS Age codes: 1=18-24, 2=25-29, ..., 13=80+)
# Simplify to broader groups
df['Age_Bracket'] = pd.cut(df['Age'], 
                            bins=[0, 4, 8, 14],  # Age codes
                            labels=['Young Adult (18-39)', 
                                   'Middle Age (40-59)', 
                                   'Older Adult (60+)'])

# 3. Behavioral Risk Score
df['Behavioral_Risk_Score'] = (
    df['Smoker'] +
    df['HvyAlcoholConsump'] +
    (1 - df['PhysActivity']) +      # Not active = risk
    (1 - df['Fruits']) +             # No fruits = risk
    (1 - df['Veggies'])              # No veggies = risk
)

# 4. Clinical Risk Score
df['Clinical_Risk_Score'] = (
    df['HighBP'] +
    df['HighChol'] +
    df['Stroke'] +
    df['HeartDiseaseorAttack'] +
    (df['BMI'] > 30).astype(int)
)

# 5. Total Risk Score
df['Total_Risk_Score'] = df['Behavioral_Risk_Score'] + df['Clinical_Risk_Score']

# 6. Healthy Lifestyle Indicator (all good behaviors)
df['Healthy_Lifestyle'] = (
    (df['PhysActivity'] == 1) & 
    (df['Fruits'] == 1) & 
    (df['Veggies'] == 1) & 
    (df['Smoker'] == 0) &
    (df['HvyAlcoholConsump'] == 0)
).astype(int)

# 7. Socioeconomic Status Index (normalized 0-1)
df['SES_Index'] = ((df['Education'] - 1) / 5 + (df['Income'] - 1) / 7) / 2

# 8. Healthcare Access Score
df['Healthcare_Access'] = (
    df['AnyHealthcare'] +
    (1 - df['NoDocbcCost'])  # No cost barrier = better access
) / 2

# Save with new features
df.to_csv('diabetes_health_indicators_with_features.csv', index=False)
print(f"✓ Saved with {len(df.columns)} columns (added {len(df.columns) - 22} features)")
print("\nNew features summary:")
print(df[['Total_Risk_Score', 'Healthy_Lifestyle', 'SES_Index']].describe())