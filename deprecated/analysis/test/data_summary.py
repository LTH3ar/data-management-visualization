import pandas as pd

def generate_summary_report():
    """Generate comprehensive data summary"""
    
    with open('data_summary_report.txt', 'w') as f:
        f.write("="*80 + "\n")
        f.write("DATA SUMMARY REPORT\n")
        f.write("Diabetes Risk Factors Analysis\n")
        f.write("="*80 + "\n\n")
        
        # Pima Dataset
        df_pima = pd.read_csv('pima_diabetes_with_features.csv')
        f.write("1. PIMA INDIANS DIABETES DATASET\n")
        f.write("-"*80 + "\n")
        f.write(f"Total Records: {len(df_pima)}\n")
        f.write(f"Total Features: {len(df_pima.columns)}\n")
        f.write(f"Diabetes Cases: {df_pima['Outcome'].sum()} ({df_pima['Outcome'].mean()*100:.1f}%)\n")
        f.write(f"Non-Diabetes: {(df_pima['Outcome']==0).sum()} ({(df_pima['Outcome']==0).mean()*100:.1f}%)\n\n")
        
        f.write("Key Statistics:\n")
        f.write(df_pima[['Glucose', 'BMI', 'Age', 'Pregnancies']].describe().to_string())
        f.write("\n\n")
        
        # Health Indicators
        df_health = pd.read_csv('diabetes_health_indicators_with_features.csv')
        f.write("2. HEALTH INDICATORS DATASET (BRFSS 2015)\n")
        f.write("-"*80 + "\n")
        f.write(f"Total Records: {len(df_health)}\n")
        f.write(f"Total Features: {len(df_health.columns)}\n")
        f.write(f"Diabetes Cases: {df_health['Diabetes_binary'].sum()} ({df_health['Diabetes_binary'].mean()*100:.1f}%)\n")
        f.write(f"Non-Diabetes: {(df_health['Diabetes_binary']==0).sum()} ({(df_health['Diabetes_binary']==0).mean()*100:.1f}%)\n\n")
        
        f.write("Risk Score Summary:\n")
        f.write(df_health[['Behavioral_Risk_Score', 'Clinical_Risk_Score', 'Total_Risk_Score']].describe().to_string())
        f.write("\n\n")
        
        # Global Prevalence
        df_global = pd.read_csv('world_diabetes_with_features.csv')
        f.write("3. GLOBAL DIABETES PREVALENCE DATASET\n")
        f.write("-"*80 + "\n")
        f.write(f"Total Countries: {len(df_global)}\n")
        f.write(f"Time Points: 2011, 2024\n")
        f.write(f"Mean Prevalence 2011: {df_global['2011'].mean():.2f}%\n")
        f.write(f"Mean Prevalence 2024: {df_global['2024'].mean():.2f}%\n")
        f.write(f"Mean Absolute Change: {df_global['Absolute_Change'].mean():.2f}%\n")
        f.write(f"Mean Percent Change: {df_global['Percent_Change'].mean():.2f}%\n\n")
        
        f.write("Top 5 Countries (2024):\n")
        for idx, row in df_global.nlargest(5, '2024').iterrows():
            f.write(f"  {row['Entity']}: {row['2024']:.1f}%\n")
        
        f.write("\nBottom 5 Countries (2024):\n")
        for idx, row in df_global.nsmallest(5, '2024').iterrows():
            f.write(f"  {row['Entity']}: {row['2024']:.1f}%\n")
    
    print("✓ Generated: data_summary_report.txt")

if __name__ == "__main__":
    generate_summary_report()
