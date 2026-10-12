import duckdb
import csv
import os

# 1. Establish project directory structure
os.makedirs('data/raw', exist_ok=True)
os.makedirs('data/processed', exist_ok=True)

raw_file = 'data/raw/sales.csv'

# 2. Generate a sample raw CSV file using a context manager
with open(raw_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['order_id', 'product', 'amount', 'date'])
    writer.writerow([1, 'Laptop', 1200.50, '2026-10-12'])
    writer.writerow([2, 'Mouse', 25.00, '2026-10-12'])
    writer.writerow([3, 'Keyboard', 75.00, '2026-10-13'])
    writer.writerow([4, 'Laptop', 1200.50, '2026-10-13'])

print("Raw CSV generated.")

# 3. Execute DuckDB transformation using read_csv_auto
print("Running DuckDB transformation...")
transform_query = f"""
    COPY (
        SELECT 
            product, 
            COUNT(*) as units_sold,
            SUM(amount) as total_revenue
        FROM read_csv_auto('{raw_file}')
        GROUP BY product
        ORDER BY total_revenue DESC
    ) TO 'data/processed/revenue_summary.parquet' (FORMAT PARQUET);
"""
duckdb.sql(transform_query)

# 4. Verify the Parquet output
verify_query = "SELECT * FROM 'data/processed/revenue_summary.parquet';"
print("\nPipeline Execution Successful. Transformed Data:")
print(duckdb.sql(verify_query).df())