import pandas as pd

df = pd.read_csv("data/vehicles.csv")

print("\n===== PRIMEIRAS LINHAS =====")
print(df.head())

print("\n===== COLUNAS =====")
print(df.columns)

print("\n===== ESTATÍSTICAS =====")
print(df.describe())

print("\n===== TIPOS =====")
print(df["type"].unique())