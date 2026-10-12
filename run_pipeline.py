import subprocess
import sys
import time

def run_script(script_name):
    print(f"\n{'='*50}")
    print(f"🚀 EXECUTING: {script_name}")
    print(f"{'='*50}")
    
    # Run the script and wait for it to finish
    result = subprocess.run([sys.executable, script_name])
    
    # Check the exit code. 0 means success. Anything else is an error.
    if result.returncode != 0:
        print(f"\n❌ PIPELINE HALTED: {script_name} failed with exit code {result.returncode}.")
        print("Fix the data or logic errors before rerunning.")
        sys.exit(1) # Abort the entire pipeline
    else:
        print(f"✅ {script_name} completed successfully.")

if __name__ == "__main__":
    start_time = time.time()
    print("Initializing End-to-End Data Pipeline Orchestration...")
    
    # The DAG: Order of execution is critical
    pipeline_steps = [
        'pipeline.py',         # Step 1: Extract & Transform (to Parquet)
        'validate_data.py',    # Step 2: Data Quality Gate
        'load_warehouse.py'    # Step 3: Idempotent Load (to Warehouse)
    ]
    
    for step in pipeline_steps:
        run_script(step)
        
    duration = round(time.time() - start_time, 2)
    print(f"\n🎉 PIPELINE SUCCESS: All steps completed in {duration} seconds.")