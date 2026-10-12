import duckdb
import sys

parquet_file = 'data/processed/revenue_summary.parquet'

print("Starting Data Quality Checks...")

# 1. Check for NULL product names
null_check = f"""
    SELECT COUNT(*) 
    FROM read_parquet('{parquet_file}') 
    WHERE product IS NULL;
"""
null_count = duckdb.sql(null_check).fetchone()[0]

if null_count > 0:
    print(f"❌ VALIDATION FAILED: Found {null_count} records with NULL product names.")
    sys.exit(1) # Halt the pipeline
else:
    print("✅ NULL Check Passed")

# 2. Check for negative or zero revenue
revenue_check = f"""
    SELECT COUNT(*) 
    FROM read_parquet('{parquet_file}') 
    WHERE total_revenue <= 0;
"""
invalid_revenue_count = duckdb.sql(revenue_check).fetchone()[0]

if invalid_revenue_count > 0:
    print(f"❌ VALIDATION FAILED: Found {invalid_revenue_count} records with zero or negative revenue.")
    sys.exit(1)
else:
    print("✅ Revenue Check Passed")

print("All Data Quality Checks Passed. Data is safe to load.")