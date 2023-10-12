import os

# needs to be before the process_data import otherwise it will create a log file
os.environ["TESTING"] = "true"

import pandas as pd
from modules.data_processing import process_data

# Additional sample datasets for testing

INVALID_LON_DATASET = {
    "lat": [10.0, 20.0, 30.0],
    "Longitude": [-190.0, 40.0, 60.0],  # Invalid longitude value
    "Volume": [100, 200, 300],
    "Type": ["supply", "demand", "SUPPLY"],
}

INVALID_VOLUME_DATASET = {
    "lat": [10.0, 20.0, 30.0],
    "lon": [-50.0, 40.0, 60.0],
    "Volume": [100, "INVALID", 300],  # Invalid volume value
    "Type": ["supply", "demand", "SUPPLY"],
}

MISSING_COLUMNS_DATASET = {
    "lat": [10.0, 20.0, 30.0],
    "lon": [-50.0, 40.0, 60.0],
    # "Volume" column missing
    "Type": ["supply", "demand", "SUPPLY"],
}

PERMISSIBLE_MISSING_TYPE_DATASET = {
    "lat": [10.0, 20.0, 30.0],
    "lon": [-50.0, 40.0, 60.0],
    "Volume": [100, 200, 300],
    "Type": ["supply", "NA", "na"],  # Permissible missing values for type
}

MIXED_MISSING_VALUES_DATASET = {
    "lat": [10.0, None, 30.0],  # Missing latitude value
    "lon": [-50.0, 40.0, "INVALID"],  # Invalid missing value representation
    "Volume": [100, 200, 300],
    "Type": ["supply", "demand", "SUPPLY"],
}


# Sample datasets for testing
VALID_DATASET = {
    "Lat": [10.0, 20.0, 30.0],
    "lon": [-50.0, 40.0, 60.0],
    "Volume": [100, 200, 300],
    "Type": ["supply", "demand", "SUPPLY"],
}

INVALID_LAT_DATASET = {
    "Latitude": [1000.0, 20.0, 30.0],  # Invalid latitude value
    "lon": [-50.0, 40.0, 60.0],
    "vol": [100, 200, 300],
    "Type": ["supply", "demand", "SUPPLY"],
}

INVALID_TYPE_DATASET = {
    "lat": [10.0, 20.0, 30.0],
    "lon": [-50.0, 40.0, 60.0],
    "Volume": [100, 200, 300],
    "Type": ["supply", "INVALID", "SUPPLY"],  # Invalid type value
}

MISSING_VALUES_DATASET = {
    "lat": [10.0, None, 30.0],  # Missing latitude value
    "lon": [-50.0, 40.0, 60.0],
    "Volume": [100, 200, 300],
    "Type": ["supply", "demand", "SUPPLY"],
}


def test_valid_dataset():
    print("Testing valid dataset...")
    df = pd.DataFrame(VALID_DATASET)
    processed_df = process_data(df)
    assert not processed_df.empty, "Valid dataset processing failed."
    print("Valid dataset passed.")


def test_invalid_lat_dataset():
    print("Testing dataset with invalid latitude...")
    df = pd.DataFrame(INVALID_LAT_DATASET)
    processed_df = process_data(df)
    assert (
        processed_df is None
    ), "Dataset with invalid latitude should not be processed."
    print("Invalid latitude dataset passed.")


def test_invalid_type_dataset():
    print("Testing dataset with invalid type...")
    df = pd.DataFrame(INVALID_TYPE_DATASET)
    processed_df = process_data(df)
    assert processed_df is None, "Dataset with invalid type should not be processed."
    print("Invalid type dataset passed.")


def test_missing_values_dataset():
    print("Testing dataset with missing values...")
    df = pd.DataFrame(MISSING_VALUES_DATASET)
    processed_df = process_data(df)

    # Check if processed_df is not None before proceeding with other assertions
    assert processed_df is not None, "Failed to process dataset with missing values."

    assert not processed_df.empty, "Dataset with missing values processing resulted in an empty dataframe."
    assert (
        len(processed_df) == len(df) - 1
    ), "Records with missing values not handled correctly."
    print("Missing values dataset passed.")


def test_invalid_lon_dataset():
    print("Testing dataset with invalid longitude...")
    df = pd.DataFrame(INVALID_LON_DATASET)
    processed_df = process_data(df)
    assert (
        processed_df is None
    ), "Dataset with invalid longitude should not be processed."
    print("Invalid longitude dataset passed.")


def test_invalid_volume_dataset():
    print("Testing dataset with invalid volume...")
    df = pd.DataFrame(INVALID_VOLUME_DATASET)
    processed_df = process_data(df)
    assert processed_df is None, "Dataset with invalid volume should not be processed."
    print("Invalid volume dataset passed.")


def test_missing_columns_dataset():
    print("Testing dataset missing mandatory columns...")
    df = pd.DataFrame(MISSING_COLUMNS_DATASET)
    processed_df = process_data(df)
    assert (
        processed_df is None
    ), "Dataset missing mandatory columns should not be processed."
    print("Missing columns dataset passed.")


def test_permissible_missing_type_dataset():
    print("Testing dataset with permissible missing type values...")
    df = pd.DataFrame(PERMISSIBLE_MISSING_TYPE_DATASET)
    processed_df = process_data(df)
    assert (
        not processed_df.empty
    ), "Dataset with permissible missing type values processing failed."
    assert len(processed_df) == len(
        df
    ), "Records with permissible missing type values not handled correctly."
    print("Permissible missing type values dataset passed.")


def test_mixed_missing_values_dataset():
    print("Testing dataset with mixed missing values...")
    df = pd.DataFrame(MIXED_MISSING_VALUES_DATASET)
    processed_df = process_data(df)
    assert (
        processed_df is None
    ), "Dataset with mixed missing values should not be processed."
    print("Mixed missing values dataset passed.")
