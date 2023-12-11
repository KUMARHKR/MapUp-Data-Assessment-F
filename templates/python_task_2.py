import pandas as pd
import numpy as np


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here



    distance_matrix = pd.DataFrame(0.0, index=df["id_start"], columns=df["id_end"])

    for index, row in df.iterrows():
        start_id = row["id_start"]
        end_id = row["id_end"]
        distance = row["distance"]

        distance_matrix.loc[start_id, end_id] = distance
        distance_matrix.loc[end_id, start_id] = distance

    return distance_matrix



def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
    unrolled_df = pd.DataFrame(columns=["id_start", "id_end", "distance"])

    for start_id in df.index:
        for end_id in df.index:
            if start_id != end_id:
                distance = df.loc[start_id, end_id]
                unrolled_df = unrolled_df.append(
                    {"id_start": start_id, "id_end": end_id, "distance": distance},
                    ignore_index=True,
                )

    return unrolled_df

def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here

    reference_avg_distance = df[df["id_start"] == reference_id]["distance"].mean()
    threshold_percentage = 0.1
    threshold_distance = reference_avg_distance * (1 + threshold_percentage)

    filtered_df = df[
        (df["id_start"] == reference_id) & (df["distance"] <= threshold_distance)
        ]
    filtered_df = filtered_df.append(
        df[
            (df["id_end"] == reference_id) & (df["distance"] <= threshold_distance)
            ]
    )

    return filtered_df.drop_duplicates()


def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here

    rate_coefficients = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }

    # Calculate toll rates based on the coefficients and distance
    for vehicle_type in rate_coefficients:
        df[vehicle_type + '_toll'] = df[vehicle_type] * rate_coefficients[vehicle_type]

    return df


def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here

    # Sample time ranges for weekdays and weekends
    weekday_time_ranges = {
        '00:00:00-10:00:00': 0.8,
        '10:00:00-18:00:00': 1.2,
        '18:00:00-23:59:59': 0.8
    }

    weekend_time_ranges = {
        '00:00:00-23:59:59': 0.7
    }

    # Assuming you have columns 'start_time' and 'end_time' in datetime.time() format
    # You may adjust the logic based on your requirements
    for index, row in df.iterrows():
        if row['start_time'] <= row['end_time']:
            time_range = f"{row['start_time']}-{row['end_time']}"
        else:
            # Handle cases where end_time crosses midnight
            time_range = f"{row['start_time']}-23:59:59,00:00:00-{row['end_time']}"

        if row['start_day'] in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
            if time_range in weekday_time_ranges:
                df.loc[index, 'toll_rate'] = df.loc[index, 'toll_rate'] * weekday_time_ranges[time_range]
        elif row['start_day'] in ['Saturday', 'Sunday']:
            if time_range in weekend_time_ranges:
                df.loc[index, 'toll_rate'] = df.loc[index, 'toll_rate'] * weekend_time_ranges[time_range]

    return df



# Read dataset-3.csv
dataset_3_path = r'C:\Users\dipku\DataspellProjects\M-project-online\MapUp-Data-Assessment-F\datasets\dataset-3.csv'
dataset_3 = pd.read_csv(dataset_3_path)

# Test the functions on dataset-3
distance_matrix = calculate_distance_matrix(dataset_3)
print("Distance Matrix:")
print(distance_matrix)

unrolled_matrix = unroll_distance_matrix(distance_matrix)
print("\nUnrolled Distance Matrix:")
print(unrolled_matrix)

reference_value = 1001400  # Replace with the desired reference value
ids_within_threshold = find_ids_within_ten_percentage_threshold(unrolled_matrix, reference_value)
print("\nIDs within Ten Percentage Threshold:")
print(ids_within_threshold)

toll_rates = calculate_toll_rate(unrolled_matrix)
print("\nToll Rates:")
print(toll_rates)

time_based_toll_rates = calculate_time_based_toll_rates(toll_rates)
print("\nTime-Based Toll Rates:")
print(time_based_toll_rates)