import pandas as pd
import numpy as np

# Load cleaned data
df = pd.read_csv('world_diabetes_cleaned_pivoted_dropped_dropped_rows.csv')

# 1. Calculate changes
df['Absolute_Change'] = df['2024'] - df['2011']
df['Percent_Change'] = ((df['2024'] - df['2011']) / df['2011']) * 100
df['Annual_Change_Rate'] = df['Absolute_Change'] / 13  # 13 years

# 2. Prevalence categories for 2024
df['Prevalence_2024_Category'] = pd.cut(df['2024'],
                                         bins=[0, 5, 10, 15, 100],
                                         labels=['Low (<5%)', 
                                                'Moderate (5-10%)', 
                                                'High (10-15%)', 
                                                'Very High (>15%)'])

# 3. Prevalence categories for 2011
df['Prevalence_2011_Category'] = pd.cut(df['2011'],
                                         bins=[0, 5, 10, 15, 100],
                                         labels=['Low (<5%)', 
                                                'Moderate (5-10%)', 
                                                'High (10-15%)', 
                                                'Very High (>15%)'])

# 4. Change direction
df['Change_Direction'] = pd.cut(df['Percent_Change'],
                                 bins=[-100, 0, 20, 50, 1000],
                                 labels=['Decreased', 
                                        'Small Increase (0-20%)', 
                                        'Moderate Increase (20-50%)', 
                                        'Large Increase (>50%)'])

# 5. Add regions (you'll need to map countries to regions)
# Simple example - you can expand this
# regions = {
#     'AFG': 'South Asia', 'ALB': 'Europe', 'DZA': 'North Africa',
#     # ... add more mappings
# }
regions = {
    # Asia
    'AFG': 'South Asia', 'ARM': 'West Asia', 'AZE': 'West Asia', 'BGD': 'South Asia',
    'BHR': 'West Asia', 'BRN': 'South East Asia', 'BTN': 'South Asia', 'CHN': 'East Asia',
    'CYP': 'West Asia', 'GEO': 'West Asia', 'HKG': 'East Asia', 'IDN': 'South East Asia',
    'IND': 'South Asia', 'IRN': 'South Asia', 'IRQ': 'West Asia', 'ISR': 'West Asia',
    'JPN': 'East Asia', 'JOR': 'West Asia', 'KAZ': 'Central Asia', 'KGZ': 'Central Asia',
    'KHM': 'South East Asia', 'KOR': 'East Asia', 'KWT': 'West Asia', 'LAO': 'South East Asia',
    'LBN': 'West Asia', 'LKA': 'South Asia', 'MAC': 'East Asia', 'MDV': 'South Asia',
    'MMR': 'South East Asia', 'MNG': 'East Asia', 'MYS': 'South East Asia', 'NPL': 'South Asia',
    'OMN': 'West Asia', 'PAK': 'South Asia', 'PHL': 'South East Asia', 'PRK': 'East Asia',
    'PSE': 'West Asia', 'QAT': 'West Asia', 'SAU': 'West Asia', 'SGP': 'South East Asia',
    'SYR': 'West Asia', 'THA': 'South East Asia', 'TJK': 'Central Asia', 'TKM': 'Central Asia',
    'TLS': 'South East Asia', 'TUR': 'West Asia', 'TWN': 'East Asia', 'ARE': 'West Asia',
    'UZB': 'Central Asia', 'VNM': 'South East Asia', 'YEM': 'West Asia',

    # Europe
    'ALB': 'Southern Europe', 'AND': 'Southern Europe', 'AUT': 'Western Europe', 'BEL': 'Western Europe',
    'BGR': 'Eastern Europe', 'BIH': 'Southern Europe', 'BLR': 'Eastern Europe', 'CHE': 'Western Europe',
    'CZE': 'Eastern Europe', 'DEU': 'Western Europe', 'DNK': 'Northern Europe', 'ESP': 'Southern Europe',
    'EST': 'Northern Europe', 'FIN': 'Northern Europe', 'FRA': 'Western Europe', 'FRO': 'Northern Europe',
    'GBR': 'Northern Europe', 'GIB': 'Southern Europe', 'GRC': 'Southern Europe', 'HRV': 'Southern Europe',
    'HUN': 'Eastern Europe', 'IMN': 'Northern Europe', 'IRL': 'Northern Europe', 'ISL': 'Northern Europe',
    'ITA': 'Southern Europe', 'LIE': 'Western Europe', 'LTU': 'Northern Europe', 'LUX': 'Western Europe',
    'LVA': 'Northern Europe', 'MCO': 'Western Europe', 'MDA': 'Eastern Europe', 'MKD': 'Southern Europe',
    'MLT': 'Southern Europe', 'MNE': 'Southern Europe', 'NLD': 'Western Europe', 'NOR': 'Northern Europe',
    'POL': 'Eastern Europe', 'PRT': 'Southern Europe', 'ROU': 'Eastern Europe', 'RUS': 'Eastern Europe',
    'SMR': 'Southern Europe', 'SRB': 'Southern Europe', 'SVK': 'Eastern Europe', 'SVN': 'Southern Europe',
    'SWE': 'Northern Europe', 'UKR': 'Eastern Europe', 'VAT': 'Southern Europe',

    # Africa
    'AGO': 'Middle Africa', 'BDI': 'East Africa', 'BEN': 'West Africa', 'BFA': 'West Africa',
    'BWA': 'South Africa', 'CAF': 'Middle Africa', 'CIV': 'West Africa', 'CMR': 'Middle Africa',
    'COD': 'Middle Africa', 'COG': 'Middle Africa', 'COM': 'East Africa', 'CPV': 'West Africa',
    'DJI': 'East Africa', 'DZA': 'North Africa', 'EGY': 'North Africa', 'ERI': 'East Africa',
    'ESH': 'North Africa', 'ETH': 'East Africa', 'GAB': 'Middle Africa', 'GHA': 'West Africa',
    'GIN': 'West Africa', 'GMB': 'West Africa', 'GNB': 'West Africa', 'GNQ': 'Middle Africa',
    'KEN': 'East Africa', 'LBR': 'West Africa', 'LBY': 'North Africa', 'LSO': 'South Africa',
    'MAR': 'North Africa', 'MDG': 'East Africa', 'MLI': 'West Africa', 'MOZ': 'East Africa',
    'MRT': 'West Africa', 'MUS': 'East Africa', 'MWI': 'East Africa', 'MYT': 'East Africa',
    'NAM': 'South Africa', 'NER': 'West Africa', 'NGA': 'West Africa', 'REU': 'East Africa',
    'RWA': 'East Africa', 'SDN': 'North Africa', 'SEN': 'West Africa', 'SLE': 'West Africa',
    'SOM': 'East Africa', 'SSD': 'East Africa', 'STP': 'Middle Africa', 'SWZ': 'South Africa',
    'SYC': 'East Africa', 'TCD': 'Middle Africa', 'TGO': 'West Africa', 'TUN': 'North Africa',
    'TZA': 'East Africa', 'UGA': 'East Africa', 'ZAF': 'South Africa', 'ZMB': 'East Africa',
    'ZWE': 'East Africa',

    # Americas
    'ABW': 'Caribbean', 'AIA': 'Caribbean', 'ARG': 'South America', 'ATG': 'Caribbean',
    'BHS': 'Caribbean', 'BLZ': 'Central America', 'BMU': 'North America', 'BOL': 'South America',
    'BRA': 'South America', 'BRB': 'Caribbean', 'CAN': 'North America', 'CHL': 'South America',
    'COL': 'South America', 'CRI': 'Central America', 'CUB': 'Caribbean', 'CUW': 'Caribbean',
    'CYM': 'Caribbean', 'DMA': 'Caribbean', 'DOM': 'Caribbean', 'ECU': 'South America',
    'GRD': 'Caribbean', 'GTM': 'Central America', 'GUF': 'South America', 'GUY': 'South America',
    'HND': 'Central America', 'HTI': 'Caribbean', 'JAM': 'Caribbean', 'KNA': 'Caribbean',
    'LCA': 'Caribbean', 'MAF': 'Caribbean', 'MEX': 'Central America', 'MSR': 'Caribbean',
    'NIC': 'Central America', 'PAN': 'Central America', 'PER': 'South America', 'PRI': 'Caribbean',
    'PRY': 'South America', 'SLV': 'Central America', 'SUR': 'South America', 'SXM': 'Caribbean',
    'TCA': 'Caribbean', 'TTO': 'Caribbean', 'URY': 'South America', 'USA': 'North America',
    'VCT': 'Caribbean', 'VEN': 'South America', 'VGB': 'Caribbean', 'VIR': 'Caribbean',

    # Oceania
    'ASM': 'Polynesia', 'AUS': 'Australia and New Zealand', 'COK': 'Polynesia', 'FJI': 'Melanesia',
    'FSM': 'Micronesia', 'GUM': 'Micronesia', 'KIR': 'Micronesia', 'MHL': 'Micronesia',
    'MNP': 'Micronesia', 'NCL': 'Melanesia', 'NRU': 'Micronesia', 'NZL': 'Australia and New Zealand',
    'PLW': 'Micronesia', 'PNG': 'Melanesia', 'PYF': 'Polynesia', 'SLB': 'Melanesia',
    'TON': 'Polynesia', 'VUT': 'Melanesia', 'WSM': 'Polynesia', 'TUV': 'Polynesia'
}
df['Region'] = df['Code'].map(regions)

# Save with new features
df.to_csv('world_diabetes_with_features.csv', index=False)
print(f"✓ Saved with {len(df.columns)} columns")
print("\nChange statistics:")
print(df[['Entity', '2011', '2024', 'Absolute_Change', 'Percent_Change']].head(10))
print(f"\nGlobal stats:")
print(f"Mean change: {df['Absolute_Change'].mean():.2f}%")
print(f"Countries with decreased prevalence: {(df['Absolute_Change'] < 0).sum()}")