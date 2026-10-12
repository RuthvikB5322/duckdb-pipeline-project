import schedule
import time
import subprocess
import sys
from datetime import datetime

def run_daily_pipeline():
    print(f"\n{'*'*50}")
    print(f"⏰ SCHEDULED TRIGGER AT: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'*'*50}")
    
    # Execute the master orchestrator we built
    subprocess.run([sys.executable, 'run_pipeline.py'])

# --- SCHEDULING LOGIC ---

# FOR TESTING: Run every 1 minute so you can watch it work immediately
schedule.every(1).minutes.do(run_daily_pipeline)

# FOR PRODUCTION: Uncomment the line below to run once a day at 3:00 AM
# schedule.every().day.at("03:00").do(run_daily_pipeline)

print(f"[{datetime.now().strftime('%H:%M:%S')}] Scheduler Daemon Started.")
print("Waiting in the background. Do not close this terminal...")

# The Daemon Loop: Keeps the script alive and checks the clock every second
while True:
    schedule.run_pending()
    time.sleep(1)