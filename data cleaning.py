-- Code Block 1: Initial Cleaning - Missing Values

import pandas as pd

# Load the dataset
data = pd.read_csv('PROJET DATA SHEET - Sheet1.csv')

# Display summary of missing values per column
print("Missing values per column:")
print(data.isnull().sum())

# Display summary of missing values per row
print("\nMissing values per row:")
print(data.isnull().sum(axis=1))

# Remove columns with the max number of missing values
max_missing_cols = data.isnull().sum().idxmax()
data = data.drop(columns=[max_missing_cols])

# Reassess missing values
print("\nMissing values after removing columns:")
print(data.isnull().sum())

# Remove rows with any missing values
data = data.dropna()

# Reassess missing values
print("\nMissing values after removing rows:")
print(data.isnull().sum())

# Save cleaned data
data.to_csv('cleaned_data.csv', index=False)

# Display final cleaned dataset
print("\nCleaned dataset:")
print(data.head())








-- Code Block 2: Handling Duplicates
# Load the cleaned dataset
cleaned_data = pd.read_csv('cleaned_data.csv')

# Check for duplicate records based on "School Name" and either "City" or "Zip Code"
duplicate_records = cleaned_data.duplicated(subset=['School Name ', 'City '], keep=False)
duplicates = cleaned_data[duplicate_records].sort_values(by=['School Name ', 'City '])

# Combine duplicate records into one record
if not duplicates.empty:
    print(f"Found {len(duplicates)} duplicate records.")
    combined_data = duplicates.groupby(['School Name ', 'City ']).agg({
        'Zip Code': 'first',
        '2022 Enrollment ': 'mean',
        'Math Score': 'mean',
        'National rank': 'mean',
        'AZ Rank': 'mean',
        'Student Teacher Ratio': 'mean',
        'Racial%-White': 'mean',
        'Racial%-Black': 'mean',
        'Racial%-Native': 'mean',
        'Racial%-Hispanic': 'mean',
        'Racial%-Asian': 'mean',
        'Racial%-Other': 'mean',
        'Lunch%-Free': 'mean',
        'Lunch%-Reduced': 'mean',
        'Lunch%-Paid': 'mean'
    }).reset_index()

    # Drop duplicate records from original dataset
    cleaned_data = cleaned_data[~duplicate_records]

    # Concatenate the combined and original datasets
    cleaned_data = pd.concat([cleaned_data, combined_data], ignore_index=True)

    print("Duplicate records combined.")
else:
    print("No duplicate records found.")

# Save the cleaned data with duplicates removed
cleaned_data.to_csv('cleaned_data_no_duplicates.csv', index=False)





--Code Block 3: Data Transformation and Type Conversion

import pandas as pd
import re
import numpy as np

# Load the cleaned dataset with no duplicate records
cleaned_data = pd.read_csv('cleaned_data_no_duplicates.csv')

# Remove special characters from numeric columns
numeric_columns = ["2022 Enrollment ", "Math Score", "National rank", "AZ Rank ", "Student Teacher Ratio",
                   "Racial%-White", "Racial%-Black", "Racial%-Native", "Racial%-Hispanic", "Racial%-Asian",
                   "Racial%-Other", "Lunch%-Free", "Lunch%-Reduced"]

for col in numeric_columns:
    cleaned_data[col] = cleaned_data[col].replace('[\$, %]', '', regex=True)
    cleaned_data[col] = cleaned_data[col].apply(lambda x: re.search(r'\d+', x).group() if isinstance(x, str) and re.search(r'\d+', x) else np.nan)
    cleaned_data[col] = cleaned_data[col].astype(float)

# Convert columns with percentage values to decimals
percentage_columns = ["Racial%-White", "Racial%-Black", "Racial%-Native", "Racial%-Hispanic", "Racial%-Asian",
                      "Racial%-Other", "Lunch%-Free", "Lunch%-Reduced"]
cleaned_data[percentage_columns] = cleaned_data[percentage_columns] / 100

# Convert "Teaching/Educational Method" column to a categorical variable
cleaned_data['Teaching/Educational Method'] = cleaned_data['Teaching/Educational Method'].astype('category')

# Drop the "Mental health services" column
cleaned_data = cleaned_data.drop(columns=['Mental health services'])

# Drop the "City" column
cleaned_data = cleaned_data.drop(columns=['City '])

# Convert "Zip Code" column to a categorical variable
cleaned_data['Zip Code'] = cleaned_data['Zip Code'].astype('category')

# Save the cleaned and transformed data to a new CSV file
cleaned_data.to_csv('cleaned_and_transformed_data.csv', index=False)

# Display the final data size and dimensions
print("Final data size and dimensions:")
print("Rows:", cleaned_data.shape[0])
print("Columns:", cleaned_data.shape[1])

