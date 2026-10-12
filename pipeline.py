import duckdb

print("--- CSV Data ---")
csv_query = """
Select *
From 'lab_sales.csv'
LIMIT 5
"""
duckdb.sql(csv_query).show()

print("\n--- Parquet Data ---")
parquet_query = """
Select *
From 'lab_sales.parquet'
LIMIT 5
"""
duckdb.sql(parquet_query).show()