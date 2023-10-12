import logging
import logging.handlers


def get_logger(
    name=__name__, log_file="supplymap.log", level=logging.INFO, formatter=None
):
    """
    Get a logger instance.

    Parameters:
    - name: Name of the logger, typically __name__.
    - log_file: Path to the log file.
    - level: Logging level, e.g., logging.INFO, logging.DEBUG.
    - formatter: Custom formatter for the log messages.

    Returns:
    - logger: A configured logger instance.
    """

    # Create or get the logger
    logger = logging.getLogger(name)

    # Avoid adding multiple handlers to the logger
    if not logger.handlers:
        # Define the default formatter if none is provided
        if not formatter:
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )

        # Create file handler for logging
        file_handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=10 * 1024 * 1024, backupCount=5
        )  # 10MB file size, keep last 5 log files
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)

        # Add the handlers to the logger
        logger.addHandler(file_handler)

        # Set level for the logger instance
        logger.setLevel(level)

    return logger
