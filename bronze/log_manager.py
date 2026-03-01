import os
import shutil
from datetime import datetime

def manage_logs():
    """
    Manages log files to prevent them from growing forever.
    If any log file is larger than 1 MB, it renames it with a timestamp
    and creates a new empty file with the original name.
    """

    # Define the maximum size for log files (1 MB = 1,048,576 bytes)
    MAX_SIZE = 1048576

    # List of log files to check and manage
    log_files = [
        "System_Log.md",
        "Logs/watcher_errors.log"
    ]

    # Process each log file
    for log_file in log_files:
        # Check if the log file exists
        if os.path.exists(log_file):
            # Get the size of the file in bytes
            file_size = os.path.getsize(log_file)

            # If the file is larger than 1 MB, archive it
            if file_size > MAX_SIZE:
                # Generate a timestamp for the archived file
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

                # Create the new filename with timestamp
                name_parts = log_file.rsplit('.', 1)  # Split on last dot
                if len(name_parts) == 2:
                    # File has an extension
                    archived_filename = f"{name_parts[0]}_{timestamp}.{name_parts[1]}"
                else:
                    # File has no extension
                    archived_filename = f"{log_file}_{timestamp}"

                # Rename the large file with the timestamp
                os.rename(log_file, archived_filename)

                # Create a new empty file with the original name
                # For System_Log.md, create with basic template
                if log_file == "System_Log.md":
                    with open(log_file, 'w', encoding='utf-8') as new_file:
                        new_file.write("# System Log\n\n## Activity Log\n\n")
                else:
                    # For other log files, create empty file
                    with open(log_file, 'w', encoding='utf-8') as new_file:
                        pass

                # Print confirmation message
                print(f"Archived large log file: {log_file} -> {archived_filename}")
            else:
                # File is within size limit, no action needed
                print(f"Log file {log_file} is within size limit ({file_size} bytes)")
        else:
            # Log file doesn't exist, create directory if needed and create empty file
            directory = os.path.dirname(log_file)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)

            # Create the appropriate empty file
            if log_file == "System_Log.md":
                with open(log_file, 'w', encoding='utf-8') as new_file:
                    new_file.write("# System Log\n\n## Activity Log\n\n")
            else:
                with open(log_file, 'w', encoding='utf-8') as new_file:
                    pass

            print(f"Created new log file: {log_file}")


if __name__ == "__main__":
    print("Starting log management...")
    manage_logs()
    print("Log management completed.")