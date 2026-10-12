import duckdb

# 1. Connect to a persistent database file (Simulating a PostgreSQL Data Warehouse)
conn = duckdb.connect('data/warehouse.db')

# 2. Define the Relational Schema (DDL)
# We enforce a PRIMARY KEY constraint to prevent duplicate product entries
conn.execute("""
    CREATE TABLE IF NOT EXISTS daily_product_revenue (
        product VARCHAR PRIMARY KEY,
        units_sold INTEGER,
        total_revenue DECIMAL(10, 2),
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
""")

print("Warehouse schema verified.")

# 3. The Idempotent Load (UPSERT)
# We read directly from the Parquet file. If the product exists, we update it. If not, we insert it.
load_query = """
    INSERT INTO daily_product_revenue (product, units_sold, total_revenue)
    SELECT product, units_sold, total_revenue 
    FROM read_parquet('data/processed/revenue_summary.parquet')
    ON CONFLICT (product) DO UPDATE 
    SET units_sold = EXCLUDED.units_sold,
        total_revenue = EXCLUDED.total_revenue,
        updated_at = CURRENT_LOCALTIMESTAMP();
"""

conn.execute(load_query)
print("Data idempotently loaded into warehouse.")

# 4. Verify the persistent data
print("\nWarehouse State:")
print(conn.execute("SELECT * FROM daily_product_revenue;").df())

conn.close()