from modules.logger import get_logger

logger = get_logger()
# Define permissible missing values
permissible_missing = {None, "", "na", "nan"}


def is_permissible_missing(value):
    """Check if a value is one of the permissible missing values."""
    return str(value).strip().lower() in permissible_missing


def validate_latitude_column(series):
    """Check if a series contains valid latitude values (-90 to 90) or permissible missing values."""
    return series.apply(
        lambda x: (isinstance(x, (int, float)) and -90 <= x <= 90)
        or is_permissible_missing(x)
    ).all()


def validate_longitude_column(series):
    """Check if a series contains valid longitude values (-180 to 180) or permissible missing values."""
    return series.apply(
        lambda x: (isinstance(x, (int, float)) and -180 <= x <= 180)
        or is_permissible_missing(x)
    ).all()


def validate_volume_column(series):
    """Check if a series contains valid volume values or permissible missing values."""
    return series.apply(
        lambda x: isinstance(x, (int, float)) or is_permissible_missing(x)
    ).all()


def validate_type_column(series):
    """Check if a series contains only 'supply' or 'demand' values, regardless of case, or permissible missing values."""
    valid_values = {"supply", "demand"}
    return series.apply(
        lambda x: str(x).strip().lower() in valid_values or is_permissible_missing(x)
    ).all()


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
    if lat_col and not validate_latitude_column(df[lat_col]):
        logger.error(f"Detected latitude column '{lat_col}' has invalid data.")
        lat_col = None

    if long_col and not validate_longitude_column(df[long_col]):
        logger.error(f"Detected longitude column '{long_col}' has invalid data.")
        long_col = None

    if volume_col and not validate_volume_column(df[volume_col]):
        logger.error(f"Detected volume column '{volume_col}' has invalid data.")
        volume_col = None

    if type_col:
        if not validate_type_column(df[type_col]):
            logger.error(
                f"Detected type column '{type_col}' has invalid entries. "
                "Only 'supply' and 'demand' are valid."
            )
            type_col = None
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
            logger.warning(f"Index {row.name}: {row.to_dict()}")

    df.dropna(inplace=True)

    return df


def process_data(df):
    """
    Process the uploaded data.
    """
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
