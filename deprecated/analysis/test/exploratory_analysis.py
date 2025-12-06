import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Create output directory for plots
import os
os.makedirs('eda_plots', exist_ok=True)

# ============================================
# PIMA DATASET EDA
# ============================================
print("="*60)
print("PIMA DATASET - EXPLORATORY ANALYSIS")
print("="*60)

df_pima = pd.read_csv('pima_diabetes_with_features.csv')

# 1. Basic statistics
print("\n1. Dataset Overview:")
print(f"   Rows: {len(df_pima)}")
print(f"   Columns: {len(df_pima.columns)}")
print(f"   Diabetes cases: {df_pima['Outcome'].sum()} ({df_pima['Outcome'].mean()*100:.1f}%)")

# 2. Distribution of continuous variables
print("\n2. Continuous Variables Summary:")
continuous_vars = ['Glucose', 'BloodPressure', 'BMI', 'Insulin', 'Age']
print(df_pima[continuous_vars].describe())

# 3. Visualizations
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
fig.suptitle('Pima Dataset - Distribution of Key Variables', fontsize=16)

# Glucose by outcome
sns.boxplot(data=df_pima, x='Outcome', y='Glucose', ax=axes[0,0])
axes[0,0].set_title('Glucose by Diabetes Status')
axes[0,0].set_xticklabels(['No Diabetes', 'Diabetes'])

# BMI by outcome
sns.boxplot(data=df_pima, x='Outcome', y='BMI', ax=axes[0,1])
axes[0,1].set_title('BMI by Diabetes Status')
axes[0,1].set_xticklabels(['No Diabetes', 'Diabetes'])

# Age by outcome
sns.boxplot(data=df_pima, x='Outcome', y='Age', ax=axes[0,2])
axes[0,2].set_title('Age by Diabetes Status')
axes[0,2].set_xticklabels(['No Diabetes', 'Diabetes'])

# BMI categories
df_pima['BMI_Category'].value_counts().plot(kind='bar', ax=axes[1,0])
axes[1,0].set_title('BMI Category Distribution')
axes[1,0].set_xlabel('BMI Category')
axes[1,0].tick_params(axis='x', rotation=45)

# Age groups
df_pima['Age_Group'].value_counts().plot(kind='bar', ax=axes[1,1])
axes[1,1].set_title('Age Group Distribution')
axes[1,1].set_xlabel('Age Group')
axes[1,1].tick_params(axis='x', rotation=45)

# Clinical Risk Score
sns.countplot(data=df_pima, x='Clinical_Risk_Score', hue='Outcome', ax=axes[1,2])
axes[1,2].set_title('Clinical Risk Score by Diabetes Status')
axes[1,2].legend(title='Diabetes', labels=['No', 'Yes'])

plt.tight_layout()
plt.savefig('eda_plots/pima_eda.png', dpi=300, bbox_inches='tight')
print("\n✓ Saved: eda_plots/pima_eda.png")

# 4. Correlation matrix
plt.figure(figsize=(10, 8))
correlation = df_pima[continuous_vars + ['Outcome']].corr()
sns.heatmap(correlation, annot=True, fmt='.2f', cmap='coolwarm', center=0)
plt.title('Correlation Matrix - Pima Dataset')
plt.tight_layout()
plt.savefig('eda_plots/pima_correlation.png', dpi=300, bbox_inches='tight')
print("✓ Saved: eda_plots/pima_correlation.png")

# ============================================
# HEALTH INDICATORS EDA
# ============================================
print("\n" + "="*60)
print("HEALTH INDICATORS - EXPLORATORY ANALYSIS")
print("="*60)

df_health = pd.read_csv('diabetes_health_indicators_with_features.csv')

print("\n1. Dataset Overview:")
print(f"   Rows: {len(df_health)}")
print(f"   Diabetes cases: {df_health['Diabetes_binary'].sum()} ({df_health['Diabetes_binary'].mean()*100:.1f}%)")

# 2. Risk score analysis
print("\n2. Risk Score Summary:")
print(df_health[['Behavioral_Risk_Score', 'Clinical_Risk_Score', 'Total_Risk_Score']].describe())

# 3. Visualizations
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
fig.suptitle('Health Indicators Dataset - Key Patterns', fontsize=16)

# Diabetes by age bracket
pd.crosstab(df_health['Age_Bracket'], df_health['Diabetes_binary'], normalize='index').plot(
    kind='bar', stacked=True, ax=axes[0,0], color=['#2ecc71', '#e74c3c'])
axes[0,0].set_title('Diabetes Rate by Age Bracket')
axes[0,0].set_ylabel('Proportion')
axes[0,0].legend(title='Diabetes', labels=['No', 'Yes'])
axes[0,0].tick_params(axis='x', rotation=45)

# Diabetes by BMI category
pd.crosstab(df_health['BMI_Category'], df_health['Diabetes_binary'], normalize='index').plot(
    kind='bar', stacked=True, ax=axes[0,1], color=['#2ecc71', '#e74c3c'])
axes[0,1].set_title('Diabetes Rate by BMI Category')
axes[0,1].set_ylabel('Proportion')
axes[0,1].legend(title='Diabetes', labels=['No', 'Yes'])
axes[0,1].tick_params(axis='x', rotation=45)

# Total Risk Score distribution
sns.histplot(data=df_health, x='Total_Risk_Score', hue='Diabetes_binary', 
             bins=15, ax=axes[0,2], multiple='dodge')
axes[0,2].set_title('Total Risk Score Distribution')
axes[0,2].legend(title='Diabetes', labels=['No', 'Yes'])

# Healthy lifestyle impact
pd.crosstab(df_health['Healthy_Lifestyle'], df_health['Diabetes_binary'], normalize='index').plot(
    kind='bar', ax=axes[1,0], color=['#2ecc71', '#e74c3c'])
axes[1,0].set_title('Diabetes Rate by Lifestyle')
axes[1,0].set_xticklabels(['Unhealthy', 'Healthy'], rotation=0)
axes[1,0].legend(title='Diabetes', labels=['No', 'Yes'])

# SES Index impact
df_health['SES_Category'] = pd.cut(df_health['SES_Index'], bins=3, labels=['Low', 'Medium', 'High'])
pd.crosstab(df_health['SES_Category'], df_health['Diabetes_binary'], normalize='index').plot(
    kind='bar', ax=axes[1,1], color=['#2ecc71', '#e74c3c'])
axes[1,1].set_title('Diabetes Rate by Socioeconomic Status')
axes[1,1].legend(title='Diabetes', labels=['No', 'Yes'])
axes[1,1].tick_params(axis='x', rotation=45)

# Healthcare access
pd.crosstab((df_health['Healthcare_Access'] > 0.5).astype(int), 
            df_health['Diabetes_binary'], normalize='index').plot(
    kind='bar', ax=axes[1,2], color=['#2ecc71', '#e74c3c'])
axes[1,2].set_title('Diabetes Rate by Healthcare Access')
axes[1,2].set_xticklabels(['Limited', 'Good'], rotation=0)
axes[1,2].legend(title='Diabetes', labels=['No', 'Yes'])

plt.tight_layout()
plt.savefig('eda_plots/health_indicators_eda.png', dpi=300, bbox_inches='tight')
print("\n✓ Saved: eda_plots/health_indicators_eda.png")

# ============================================
# GLOBAL PREVALENCE EDA
# ============================================
print("\n" + "="*60)
print("GLOBAL PREVALENCE - EXPLORATORY ANALYSIS")
print("="*60)

df_global = pd.read_csv('world_diabetes_with_features.csv')

print("\n1. Dataset Overview:")
print(f"   Countries: {len(df_global)}")
print(f"   Mean prevalence 2011: {df_global['2011'].mean():.2f}%")
print(f"   Mean prevalence 2024: {df_global['2024'].mean():.2f}%")
print(f"   Mean change: {df_global['Absolute_Change'].mean():.2f}%")

# 2. Top/Bottom countries
print("\n2. Top 10 Countries (2024 Prevalence):")
print(df_global.nlargest(10, '2024')[['Entity', '2024', 'Absolute_Change']])

print("\n3. Bottom 10 Countries (2024 Prevalence):")
print(df_global.nsmallest(10, '2024')[['Entity', '2024', 'Absolute_Change']])

print("\n4. Largest Increases:")
print(df_global.nlargest(10, 'Absolute_Change')[['Entity', '2011', '2024', 'Absolute_Change']])

# 3. Visualizations
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Global Diabetes Prevalence - Trends and Patterns', fontsize=16)

# 2011 vs 2024 scatter
axes[0,0].scatter(df_global['2011'], df_global['2024'], alpha=0.6)
axes[0,0].plot([0, 25], [0, 25], 'r--', label='No change line')
axes[0,0].set_xlabel('Prevalence 2011 (%)')
axes[0,0].set_ylabel('Prevalence 2024 (%)')
axes[0,0].set_title('2011 vs 2024 Prevalence')
axes[0,0].legend()
axes[0,0].grid(True, alpha=0.3)

# Distribution of changes
axes[0,1].hist(df_global['Absolute_Change'], bins=30, edgecolor='black')
axes[0,1].axvline(df_global['Absolute_Change'].mean(), color='r', 
                   linestyle='--', label=f'Mean: {df_global["Absolute_Change"].mean():.2f}%')
axes[0,1].set_xlabel('Absolute Change (%)')
axes[0,1].set_ylabel('Number of Countries')
axes[0,1].set_title('Distribution of Prevalence Changes (2011-2024)')
axes[0,1].legend()

# Top 15 countries in 2024
top15 = df_global.nlargest(15, '2024').sort_values('2024')
axes[1,0].barh(range(len(top15)), top15['2024'])
axes[1,0].set_yticks(range(len(top15)))
axes[1,0].set_yticklabels(top15['Entity'])
axes[1,0].set_xlabel('Prevalence (%)')
axes[1,0].set_title('Top 15 Countries by Diabetes Prevalence (2024)')
axes[1,0].grid(axis='x', alpha=0.3)

# Largest increases
top_increases = df_global.nlargest(15, 'Absolute_Change').sort_values('Absolute_Change')
axes[1,1].barh(range(len(top_increases)), top_increases['Absolute_Change'])
axes[1,1].set_yticks(range(len(top_increases)))
axes[1,1].set_yticklabels(top_increases['Entity'])
axes[1,1].set_xlabel('Absolute Change (%)')
axes[1,1].set_title('Top 15 Countries by Prevalence Increase (2011-2024)')
axes[1,1].grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig('eda_plots/global_prevalence_eda.png', dpi=300, bbox_inches='tight')
print("\n✓ Saved: eda_plots/global_prevalence_eda.png")

print("\n" + "="*60)
print("EDA COMPLETE!")
print("="*60)
print("\nGenerated files in eda_plots/:")
print("  - pima_eda.png")
print("  - pima_correlation.png")
print("  - health_indicators_eda.png")
print("  - global_prevalence_eda.png")