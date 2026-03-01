import os
import time
import random
from datetime import datetime

def log_action(message):
    """Log actions to the actions log file."""
    # Ensure logs directory exists
    if not os.path.exists("logs"):
        os.makedirs("logs")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"

    with open("logs/actions.log", "a", encoding="utf-8") as log_file:
        log_file.write(log_entry)

def trigger_ai_processing():
    """Trigger the AI processing workflow (simulated equivalent of run_ai_employee.py --once)."""
    # In a real implementation, this would call the actual AI processing
    # For now, we'll simulate by logging the action
    log_action("AI processing workflow triggered")
    print("AI processing workflow would be triggered here")

def run_vault_watcher():
    """Main function to run the vault watcher continuously."""
    inbox_folder = "AI_Employee_Vault/Inbox"

    # Ensure the monitored folder exists
    if not os.path.exists(inbox_folder):
        os.makedirs(inbox_folder)
        log_action(f"Created monitored folder: {inbox_folder}")

    # Track files that have already been processed to avoid duplicates
    processed_files = set()

    # Initialize with any existing files in the inbox
    if os.path.exists(inbox_folder):
        for filename in os.listdir(inbox_folder):
            if filename.endswith('.md'):
                file_path = os.path.join(inbox_folder, filename)
                if os.path.isfile(file_path):
                    processed_files.add(filename)

    log_action("Vault Watcher started monitoring")
    print(f"Started monitoring {inbox_folder} for new .md files...")
    print("Press Ctrl+C to stop.")

    try:
        while True:
            # Randomize the polling interval between 10-30 seconds for production readiness
            sleep_time = random.randint(10, 30)

            # Check if the monitored folder exists
            if not os.path.exists(inbox_folder):
                os.makedirs(inbox_folder)
                log_action(f"Recreated monitored folder: {inbox_folder}")

            # Get current list of .md files in the inbox
            current_md_files = set()
            for filename in os.listdir(inbox_folder):
                if filename.endswith('.md'):
                    file_path = os.path.join(inbox_folder, filename)
                    if os.path.isfile(file_path):
                        current_md_files.add(filename)

            # Find new .md files that weren't there before
            new_files = current_md_files - processed_files

            # Process each new file
            for filename in new_files:
                file_path = os.path.join(inbox_folder, filename)

                # Verify it's still a file (hasn't been moved/deleted)
                if os.path.isfile(file_path):
                    print(f"New .md file detected: {filename}")
                    log_action(f"New .md file detected: {filename}")

                    # Trigger the AI processing workflow
                    trigger_ai_processing()

                    # Add to the processed set to avoid processing the same file twice
                    processed_files.add(filename)

            # Sleep for the randomized interval before checking again
            time.sleep(sleep_time)

    except KeyboardInterrupt:
        log_action("Vault Watcher stopped by user")
        print("\nVault Watcher stopped.")

if __name__ == "__main__":
    run_vault_watcher()