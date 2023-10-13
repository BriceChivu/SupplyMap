# This is the data_processing.py file.

from modules.logger import get_logger

logger = get_logger()
# Define permissible missing values
permissible_missing = {None, "", "na", "nan"}


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


def validate_latitude_column(series):
    """Check if a series contains valid latitude values (-90 to 90) or permissible missing values."""
    invalid_entries = series[
        ~series.apply(lambda x: is_valid_latitude(x) or is_permissible_missing(x))
    ]
    return invalid_entries.empty, invalid_entries


def validate_longitude_column(series):
    """Check if a series contains valid longitude values (-180 to 180) or permissible missing values."""
    invalid_entries = series[
        ~series.apply(lambda x: is_valid_longitude(x) or is_permissible_missing(x))
    ]
    return invalid_entries.empty, invalid_entries


def validate_type_column(series):
    """Check if a series contains valid type values ('supply' or 'demand') or permissible missing values."""
    invalid_entries = series[
        ~series.apply(lambda x: is_valid_type(x) or is_permissible_missing(x))
    ]
    return invalid_entries.empty, invalid_entries


def validate_volume_column(series):
    """Check if a series contains valid volume values (numeric) or permissible missing values."""
    invalid_entries = series[
        ~series.apply(lambda x: is_valid_volume(x) or is_permissible_missing(x))
    ]
    return invalid_entries.empty, invalid_entries


def detect_and_validate_columns(df):
    """
    Detect and validate necessary columns.
    """
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

    # Validate detected columns
    valid_lat, invalid_lat_entries = validate_latitude_column(df[lat_col])
    if lat_col and not valid_lat:
        logger.error(
            f"Invalid data found in the latitude column '{lat_col}': {invalid_lat_entries.to_dict()}. Valid entries are between -90 and 90."
        )

    valid_lon, invalid_lon_entries = validate_longitude_column(df[long_col])
    if long_col and not valid_lon:
        logger.error(
            f"Invalid data found in the longitude column '{long_col}': {invalid_lon_entries.to_dict()}. Valid entries are between -180 and 180."
        )

    valid_vol, invalid_vol_entries = validate_volume_column(df[volume_col])
    if volume_col and not valid_vol:
        logger.error(
            f"Invalid data found in the volume column '{volume_col}': {invalid_vol_entries.to_dict()}. Valid entries are non-negative numbers."
        )

    valid_type, invalid_type_entries = validate_type_column(df[type_col])
    if type_col and not valid_type:
        logger.error(
            f"Invalid entries detected in the type column '{type_col}': {invalid_type_entries.to_dict()}. Valid entries are 'supply' and 'demand'."
        )

    else:
        df["type"] = "demand"
        type_col = "type"

    # Log detected and validated columns
    logger.info(f"Using '{lat_col}' as latitude column.")
    logger.info(f"Using '{long_col}' as longitude column.")
    logger.info(f"Using '{volume_col}' as volume column.")
    logger.info(f"Using '{type_col}' as type column.")

    return lat_col, long_col, volume_col, type_col


def handle_missing_values(df):
    """
    Drop records with missing values and log the details of the dropped records.
    """
    missing_data_records = df[df.isnull().any(axis=1)]

    if not missing_data_records.empty:
        logger.warning("Records with missing values detected:")
        for _, row in missing_data_records.iterrows():
            # Adjust the index for better reference to the displayed DataFrame
            adjusted_index = row.name + 2
            logger.warning(f"Row {adjusted_index}: {row.to_dict()}")

    df.dropna(inplace=True)

    return df


def process_data(df):
    """
    Process the uploaded data.
    """
    # Log the dataset being processed
    logger.info("===========================================")
    logger.info("Processing a new dataset...")

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

    # Handle missing values
    df = handle_missing_values(df)

    # Return the processed dataframe
    return df[[lat_col, long_col, volume_col, type_col]]
