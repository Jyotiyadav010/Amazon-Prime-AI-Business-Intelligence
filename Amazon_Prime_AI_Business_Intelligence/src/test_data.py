import pandas as pd

titles = pd.read_excel("data/titles.xlsx")
credits = pd.read_excel("data/credits.xlsx")

print("Titles Shape:", titles.shape)
print("Credits Shape:", credits.shape)

print("\nTitles Columns:")
print(titles.columns.tolist())

print("\nCredits Columns:")
print(credits.columns.tolist())

print("\nFirst 5 Titles:")
print(titles.head())

print("\nFirst 5 Credits:")
print(credits.head())
print("\nTitles Dataset Columns:")
print(titles.columns.tolist())

print("\nCredits Dataset Columns:")
print(credits.columns.tolist())

print("\nDataset Shape:")
print("Titles:", titles.shape)
print("Credits:", credits.shape)