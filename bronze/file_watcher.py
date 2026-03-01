import os
import time
from datetime import datetime

def log_error(error_message):
    """Logs error messages with timestamp to the error log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    error_log_entry = f"[{timestamp}] ERROR: {error_message}\n"

    # Ensure Logs directory exists
    if not os.path.exists("Logs"):
        os.makedirs("Logs")

    # Write error message to the log file
    with open("Logs/watcher_errors.log", "a", encoding="utf-8") as log_file:
        log_file.write(error_log_entry)

def create_task_file(filename):
    """Creates a task file in the Needs_Action folder for a new inbox file."""
    try:
        # Create the task file content with frontmatter using the new template
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        task_content = f"""---
type: file_review
status: pending
priority: medium
created_at: {timestamp}
related_files: ["Inbox/{filename}"]
---

# Review File: {filename}

## Description
A new file was added to the Inbox folder that requires review and action determination.

## CheckList
- [ ] Review the content of {filename}
- [ ] Determine appropriate action based on content
- [ ] Execute necessary follow-up actions

## Notes
File {filename} was detected in the Inbox folder and requires processing.
"""

        # Create the task file in the Needs_Action folder
        task_filename = f"task_{os.path.splitext(filename)[0]}_{int(time.time())}.md"
        task_path = os.path.join("Needs_Action", task_filename)

        with open(task_path, 'w', encoding='utf-8') as task_file:
            task_file.write(task_content)

        print(f"Created task file: {task_filename}")

    except Exception as e:
        # If there's an error creating the task file, log it
        error_msg = f"Failed to create task file for {filename}: {str(e)}"
        log_error(error_msg)
        print(f"Error: {error_msg}")

def monitor_inbox():
    """Monitors the Inbox folder for new files and creates task files."""
    try:
        # Track files that have already been processed to avoid duplicates
        processed_files = set()

        # Initialize with any existing files in the Inbox
        if os.path.exists("Inbox"):
            for filename in os.listdir("Inbox"):
                file_path = os.path.join("Inbox", filename)
                if os.path.isfile(file_path):
                    processed_files.add(filename)
        else:
            # If Inbox doesn't exist, create it automatically
            os.makedirs("Inbox")
            print("Inbox folder did not exist. Created automatically.")
            return

        print("Starting file watcher for Inbox folder...")
        print("Press Ctrl+C to stop.")

        while True:
            # Check if the Inbox folder exists, create if missing
            if not os.path.exists("Inbox"):
                os.makedirs("Inbox")
                print("Inbox folder was missing. Recreated automatically.")
                # Reset processed files since folder was recreated
                processed_files.clear()

            # Get current list of files in the Inbox
            current_files = set(os.listdir("Inbox"))

            # Find new files that weren't there before
            new_files = current_files - processed_files

            # Process each new file
            for filename in new_files:
                file_path = os.path.join("Inbox", filename)

                # Make sure it's a file, not a subdirectory
                if os.path.isfile(file_path):
                    print(f"New file detected: {filename}")
                    create_task_file(filename)

                    # Add to the processed set to avoid creating duplicate tasks
                    processed_files.add(filename)

            # Wait for 5 seconds before checking again
            time.sleep(5)

    except KeyboardInterrupt:
        print("\nFile watcher stopped by user.")
    except Exception as e:
        # Catch any unexpected errors in the main loop and log them
        error_msg = f"Unexpected error in monitor_inbox: {str(e)}"
        log_error(error_msg)
        print(f"Error: {error_msg}")

if __name__ == "__main__":
    # Make sure both Inbox and Needs_Action folders exist
    # Create them automatically if they don't exist
    if not os.path.exists("Inbox"):
        os.makedirs("Inbox")
        print("Created Inbox folder.")

    if not os.path.exists("Needs_Action"):
        os.makedirs("Needs_Action")
        print("Created Needs_Action folder.")

    # Start monitoring the Inbox
    try:
        monitor_inbox()
    except Exception as e:
        # Log any errors that occur during execution
        error_msg = f"Critical error during execution: {str(e)}"
        log_error(error_msg)
        print(f"Critical error: {error_msg}")