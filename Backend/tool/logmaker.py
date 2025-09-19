import os

def log(filename: str, log_message: str):
    """
    Save debug logs to specified file.

    This function creates a folder named 'logs' (if it doesn't exist)
    and saves log messages with the specified filename inside it.
    If the file already exists, it overwrites the content.

    Args:
        filename (str): The name of the file to save the log to. (e.g., 'app.log')
        log_message (str): The log string to save to the file.
    """
    # Name of the folder to save logs
    log_dir = 'logs'

    # Create 'logs' folder if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)

    # Generate complete file path (handle path separators for the operating system)
    file_path = os.path.join(log_dir, filename)
    # Add '.log' extension if filename is empty or has no extension
    file_path += '.log'

    try:
        # Open file in write mode ('w') to write log message.
        # 'w' mode overwrites existing content if file exists.
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(log_message)
        print(f"Log successfully saved to '{file_path}'.")
    except IOError as e:
        print(f"An error occurred while writing file: {e}")

# --- Function usage examples ---
if __name__ == "__main__":
    # Save first log
    error_log = "[ERROR] User authentication failed. User ID: 'user123'"
    log('error.log', error_log)

    # Save second log (different file)
    info_log = "[INFO] Application started. Version: 1.0.2"
    log('info.log', info_log)

    # Overwrite existing log file
    updated_error_log = "[ERROR] Database connection timeout. (1 retry attempt)"
    log('error.log', updated_error_log)