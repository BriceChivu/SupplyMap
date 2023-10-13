import pandas as pd
import random
import numpy as np


# Randomly assign missing values
def random_nan(val):
    return val if random.random() > 0.2 else np.nan


data1 = {
    "lat": [random_nan(i) for i in range(1, 51)],
    "lon": [random_nan(i) for i in range(-50, 0)],
    "Volume": [random_nan(i * 100) for i in range(1, 51)],
    "Type": [random.choice(["supply", "demand", None]) for _ in range(1, 51)],
}
df1 = pd.DataFrame(data1)
df1.to_csv("tests/dummy_data/datasets/dataset1.csv", index=False)

data2 = {
    "lat": [
        random.choice([i, i * 1000]) for i in range(1, 51)
    ],  # Introduce some invalid latitudes
    "lon": [
        random.choice([i, i * 1000]) for i in range(-50, 0)
    ],  # Introduce some invalid longitudes
    "Volume": [i * 100 for i in range(1, 51)],
    "Type": [
        random.choice(["supply", "demand", "INVALID"]) for _ in range(1, 51)
    ],  # Introduce some invalid types
}
df2 = pd.DataFrame(data2)
df2.to_csv("tests/dummy_data/datasets/dataset2.csv", index=False)

data3 = {
    "lat": [
        random.choice([i, "N/A"]) for i in range(1, 51)
    ],  # Using string "N/A" for missing values
    "lon": [
        random.choice([i, ""]) for i in range(-50, 0)
    ],  # Using empty string for missing values
    "Volume": [i * 100 for i in range(1, 51)],
    "Type": [
        random.choice(["supply", "demand", "na"]) for _ in range(1, 51)
    ],  # Using "na" for missing values
}
df3 = pd.DataFrame(data3)
df3.to_csv("tests/dummy_data/datasets/dataset3.csv", index=False)

data4 = {
    "lat": [i for i in range(1, 51)],
    "lon": [i for i in range(-50, 0)],
    "Volume": [i * 100 for i in range(1, 51)],
    "Type": [random.choice(["supply", "demand"]) for _ in range(1, 51)],
    "Extra_Column1": [
        random.choice(["A", "B", "C"]) for _ in range(1, 51)
    ],  # Unnecessary column
    "Extra_Column2": [
        random.choice(["X", "Y", "Z"]) for _ in range(1, 51)
    ],  # Another unnecessary column
}
df4 = pd.DataFrame(data4)
df4.to_csv("tests/dummy_data/datasets/dataset4.csv", index=False)

data5 = {
    "lat": [
        random.choice([i, str(i)]) for i in range(1, 51)
    ],  # Mixing float and string types
    "lon": [
        random.choice([i, str(i)]) for i in range(-50, 0)
    ],  # Mixing float and string types
    "Volume": [i * 100 for i in range(1, 51)],
    "Type": [random.choice(["supply", "demand"]) for _ in range(1, 51)],
}
df5 = pd.DataFrame(data5)
df5.to_csv("tests/dummy_data/datasets/dataset5.csv", index=False)

print(
    "Datasets generated: dataset1.csv, dataset2.csv, dataset3.csv, dataset4.csv, dataset5.csv"
)
