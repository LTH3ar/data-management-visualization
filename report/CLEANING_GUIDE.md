# 🧹 DATA CLEANING GUIDE

## ⚡ QUICK START (2 MINUTES)

### **Run These 2 Scripts:**

```bash
# Step 1: Check what needs cleaning
python 01_inspect_data.py

# Step 2: Clean everything
python 02_clean_data.py
```

**That's it!** Your data will be cleaned and ready! ✅

---

## 📊 WHAT EACH DATASET NEEDS

### **Dataset 1: Pima Indians** ⚠️⚠️⚠️ **CRITICAL CLEANING NEEDED**

**Problems:**
- ❌ Contains **impossible zeros** (Glucose=0, BMI=0, etc.)
- ❌ These are actually **missing values disguised as zeros**
- ❌ Will **ruin your analysis** if not fixed!

**Example:**
```
Person with Glucose = 0 is DEAD, not diabetic!
Person with BMI = 0 doesn't exist!
```

**Solution:**
✅ Replace zeros with NaN
✅ Either drop rows OR impute median values

**You'll get 2 versions:**
1. `pima_diabetes_clean.csv` - 392 rows (dropped missing)
2. `pima_diabetes_imputed.csv` - 768 rows (filled missing) ← **Use this!**

---

### **Dataset 2: CDC Health Indicators** ✅ **ALREADY CLEAN!**

**Status:**
- ✅ No missing values
- ✅ All data valid
- ✅ Just needs verification

**Optional:**
- Created a 10k sample for faster testing
- Full dataset has 253k rows (may be slow)

**You'll get 2 versions:**
1. `cdc_diabetes_clean.csv` - Full 253k rows
2. `cdc_diabetes_sample.csv` - 10k sample ← **Use for testing**

---

### **Dataset 3: World Diabetes** ⚠️⚠️ **MODERATE CLEANING NEEDED**

**Problems:**
- ❌ Contains **regional aggregates** (not actual countries)
- ❌ Has "World", "Africa", "High income" etc.
- ❌ Some missing values

**Example Bad Rows:**
```
World               - Not a country!
Sub-Saharan Africa  - Region, not country!
High income         - Income group, not country!
```

**Solution:**
✅ Filter to actual countries only
✅ Remove regional aggregates
✅ Keep years 2000-2024
✅ Drop rows with missing prevalence

**You'll get:**
1. `world_diabetes_clean.csv` - Real countries only

---

## 🎯 CLEANING SUMMARY

| Dataset | Issue | Action | Output File |
|---------|-------|--------|-------------|
| **Pima** | Impossible zeros | Replace & impute | `pima_diabetes_imputed.csv` |
| **CDC** | Already clean | Verify + sample | `cdc_diabetes_sample.csv` |
| **World** | Regional data | Filter countries | `world_diabetes_clean.csv` |

---

## 📁 BEFORE vs AFTER

### **Before Cleaning:**
```
data/
├── pima_diabetes.csv                                 (768 rows, has zeros)
├── diabetes_binary_health_indicators_BRFSS2015.csv   (253k rows)
└── world_diabetes.csv                                (messy, has regions)
```

### **After Cleaning:**
```
data/
├── pima_diabetes.csv                    (original)
├── pima_diabetes_clean.csv              (392 rows, dropped missing)
├── pima_diabetes_imputed.csv            (768 rows, filled missing) ✅ USE THIS
├── diabetes_binary_health_indicators_BRFSS2015.csv (original)
├── cdc_diabetes_clean.csv               (253k rows, full)
├── cdc_diabetes_sample.csv              (10k rows, sample) ✅ USE THIS
├── world_diabetes.csv                   (original)
└── world_diabetes_clean.csv             (clean countries only) ✅ USE THIS
```

---

## 🔍 VERIFICATION EXAMPLES

### **Check Pima Cleaning Worked:**

```python
import pandas as pd

# Load cleaned data
df = pd.read_csv('pima_diabetes_imputed.csv')

# Check for zeros in biological measurements
print(df['Glucose'].min())      # Should NOT be 0
print(df['BMI'].min())          # Should NOT be 0
print(df['BloodPressure'].min()) # Should NOT be 0

# Should all be > 0 now!
```

### **Check World Cleaning Worked:**

```python
import pandas as pd

# Load cleaned data
df = pd.read_csv('world_diabetes_clean.csv')

# Check countries
print(df['Country'].unique())

# Should NOT see: 'World', 'Africa', 'High income', etc.
# Should ONLY see: 'Afghanistan', 'Albania', 'Algeria', etc.
```

---

## 💡 WHICH FILES TO USE FOR ANALYSIS?

### **For Your Project, Use These:**

1. ✅ `pima_diabetes_imputed.csv` 
   - Keep all 768 rows
   - Missing values filled with median
   
2. ✅ `cdc_diabetes_sample.csv`
   - 10k rows for faster testing
   - Use full dataset later if needed
   
3. ✅ `world_diabetes_clean.csv`
   - Real countries only
   - Years 2000-2024

---

## ⏰ TIME ESTIMATE

| Task | Time |
|------|------|
| Run inspection script | 30 seconds |
| Run cleaning script | 1 minute |
| Verify cleaned files | 1 minute |
| **TOTAL** | **2-3 minutes** |

---

## 🆘 TROUBLESHOOTING

### **Error: "File not found"**
**Solution:** Make sure your CSV files are in the same folder as the Python scripts!

```
your_folder/
├── pima_diabetes.csv
├── diabetes_binary_health_indicators_BRFSS2015.csv
├── world_diabetes.csv
├── 01_inspect_data.py
└── 02_clean_data.py
```

### **Error: "No module named pandas"**
**Solution:** Install required packages:
```bash
pip install pandas numpy scikit-learn
```

### **World dataset columns look different**
**Solution:** The script auto-detects column names. If it fails, check what your columns are actually called and let me know!

---

## ✅ SUCCESS CHECKLIST

After running both scripts, verify:

- [ ] No more zeros in Pima biological measurements
- [ ] Pima dataset has 768 rows (imputed version)
- [ ] CDC sample has 10,000 rows (balanced)
- [ ] World dataset has NO regional aggregates
- [ ] World dataset only has years 2000+
- [ ] All 6 new files created successfully
