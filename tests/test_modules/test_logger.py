import os
from modules.logger import get_logger


def test_get_logger():
    # Define log file path
    log_file = "test_supply_chain_app.log"

    # Get a logger instance
    logger = get_logger(log_file=log_file)

    # Log a test message
    test_msg = "This is a test log message."
    logger.info(test_msg)

    # Check if the log file is created
    assert os.path.exists(log_file)

    # Read the log file content
    with open(log_file, "r") as file:
        logs = file.read()


    # Check if the test message is in the logs
    assert test_msg in logs

    # Clean up by removing the test log file
    os.remove(log_file)


def test_rotating_file_handler():
    # Define log file path
    log_file = "test_supply_chain_app.log"
    
    # Get a logger instance
    logger = get_logger(log_file=log_file)
    
    # Log a large message repeatedly to exceed the maxBytes limit
    test_msg = "This is a test log message." * 1000000  # Create a large message
    for _ in range(10):  # Log the message multiple times
        logger.info(test_msg)
    
    # Check if the backup files have been created
    backup_files = [f"{log_file}.{i}" for i in range(1, 6)]  # .1, .2, ... .5
    backup_files_exist = all([os.path.exists(file) for file in backup_files])
    
    # Check if no additional backup file is created (i.e., only 5 backup files)
    no_extra_backup = not os.path.exists(f"{log_file}.6")
    
    assert backup_files_exist
    assert no_extra_backup
    
    # Clean up by removing the test log files
    os.remove(log_file)
    for file in backup_files:
        os.remove(file)
