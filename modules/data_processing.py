from modules.logger import get_logger

logger = get_logger()

# Define permissible missing values
permissible_missing = {None, "", "na", "nan", "n/a"}


def is_permissible_missing(value):
    """Check if a value is one of the permissible missing values."""
    return str(value).strip().lower() in permissible_missing


def is_valid_latitude(value):
    """Check if a value is a valid latitude (-90 to 90)."""
    try:
        value = float(str(value).strip())
        return -90 <= value <= 90
    except ValueError:
        return False


def is_valid_longitude(value):
    """Check if a value is a valid longitude (-180 to 180)."""
    try:
        value = float(str(value).strip())
        return -180 <= value <= 180
    except ValueError:
        return False


def is_valid_type(value):
    """Check if a value is a valid type ('supply' or 'demand')."""
    value = str(value).strip().lower()
    return value in ["supply", "demand"]


def is_valid_volume(value):
    """Check if a value is a valid volume (numeric and non-negative)."""
    try:
        volume = float(str(value).strip())
        return volume >= 0
    except ValueError:
        return False


def log_invalid_entries(df, validation_function, column_name, valid_description):
    """Log invalid entries for a given column."""
    invalid_entries = df[
        ~df[column_name].apply(
            lambda x: validation_function(x) or is_permissible_missing(x)
        )
    ]

    if not invalid_entries.empty:
        logger.error(
            f"Invalid data found in the column '{column_name}': {invalid_entries.to_dict()}. {valid_description}"
        )

    return (
        invalid_entries.index
    )  # Return indices of invalid entries for further processing


def clean_dataframe(df, invalid_indices):
    """Drop rows with invalid entries based on provided indices and rows with permissible missing values."""

    # Drop rows with invalid indices
    df.drop(invalid_indices, inplace=True, errors="ignore")

    # Drop rows with permissible missing values
    for column in df.columns:
        permissible_missing_indices = df[df[column].apply(is_permissible_missing)].index
        df.drop(permissible_missing_indices, inplace=True, errors="ignore")

    return df


def detect_and_validate_columns(df):
    # Define valid column names
    valid_lat_names = ["lat", "Lat", "Latitude", "latitude"]
    valid_lon_names = ["lon", "Lon", "long", "Long", "Longitude", "longitude"]
    valid_vol_names = ["volume", "Volume", "vol", "Vol"]
    valid_type_names = ["type", "Type"]

    # Detect columns based on valid names
    lat_col = next((col for col in df.columns if col in valid_lat_names), None)
    long_col = next((col for col in df.columns if col in valid_lon_names), None)
    volume_col = next((col for col in df.columns if col in valid_vol_names), None)
    type_col = next((col for col in df.columns if col in valid_type_names), None)

    # Log invalid entries for detected columns
    invalid_lat_indices = log_invalid_entries(
        df, is_valid_latitude, lat_col, "Valid entries are between -90 and 90."
    )
    invalid_long_indices = log_invalid_entries(
        df, is_valid_longitude, long_col, "Valid entries are between -180 and 180."
    )
    invalid_vol_indices = log_invalid_entries(
        df, is_valid_volume, volume_col, "Valid entries are non-negative numbers."
    )
    invalid_type_indices = log_invalid_entries(
        df, is_valid_type, type_col, "Valid entries are 'supply' and 'demand'."
    )

    # Aggregate all invalid indices
    all_invalid_indices = (
        set(invalid_lat_indices)
        | set(invalid_long_indices)
        | set(invalid_vol_indices)
        | set(invalid_type_indices)
    )

    # Clean the dataframe
    df = clean_dataframe(df, all_invalid_indices)

    # Log detected and validated columns
    logger.info(f"Using '{lat_col}' as latitude column.")
    logger.info(f"Using '{long_col}' as longitude column.")
    logger.info(f"Using '{volume_col}' as volume column.")
    logger.info(f"Using '{type_col}' as type column.")

    return lat_col, long_col, volume_col, type_col


def process_data(df, filename):
    # Log the dataset being processed
    logger.info("===========================================")
    logger.info(f"Processing {filename}...")

    # Create a deep copy of the DataFrame to avoid modifying the original
    df = df.copy(deep=True)

    # Detect and validate columns
    lat_col, long_col, volume_col, type_col = detect_and_validate_columns(df)

    # Ensure necessary columns were detected and validated
    if not all([lat_col, long_col, volume_col, type_col]):
        logger.error(
            "Failed to detect or validate all necessary columns. Processing halted."
        )
        return None

    # Return the processed dataframe
    return df[[lat_col, long_col, volume_col, type_col]]
