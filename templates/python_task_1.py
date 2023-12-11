from datetime import timedelta

import pandas as pd
import numpy as np


def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here
    car_matrix = df.pivot_table(
        values="car", index="id_1", columns="id_2", fill_value=0
    )

    # Set diagonal values to 0
    np.fill_diagonal(car_matrix.values, 0)

    return car_matrix




def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    car_types = {
        "low": df.query("car <= 15")["car"].count(),
        "medium": df.query("15 < car <= 25")["car"].count(),
        "high": df.query("car > 25")["car"].count(),
    }

    return car_types


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
    mean_bus_value = df["bus"].mean()
    exceeding_indexes = df.query("bus > 2 * @mean_bus_value").index.tolist()

    return sorted(exceeding_indexes)


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    avg_truck_by_route = df.groupby("route")["truck"].mean()
    filtered_routes = avg_truck_by_route[avg_truck_by_route > 7].index.tolist()

    return sorted(filtered_routes)


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    def multiplier(value):
        if value > 20:
            return value * 0.75
        elif value <= 20:
            return value * 1.25
        else:
            return value

    return matrix.applymap(lambda value: multiplier(value)).round(1)

def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
    def is_valid_time_range(row):

        start_time = pd.to_datetime(row["startDay"] + " " + row["startTime"])
        end_time = pd.to_datetime(row["endDay"] + " " + row["endTime"])

        return (
                (end_time - start_time) >= timedelta(days=1)
                and start_time.time() <= end_time.time() <= start_time.time() + timedelta(hours=23, minutes=59, seconds=59)
        )
