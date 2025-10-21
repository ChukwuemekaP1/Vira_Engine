# SPRINT 1, TASK 1.1
# VERA AI - DATA GENERATION SCRIPT
# This script generates the mock land registry CSV file.

import pandas as pd
from faker import Faker
import random
import os

# --- Configuration ---
# Total number of rows in the final CSV file.
NUM_TOTAL_ROWS = 8500
# The folder where our generated data will be stored.
OUTPUT_FOLDER = "nigeria_demo_data"
# The name of the output file.
OUTPUT_FILENAME = "Nigerian_Land_Registry_Mock.csv"

# --- Golden Records Definition ---
# This list contains the 5 specific scenarios we want to embed in our data.
# Each dictionary is a "golden record" that the AI will later analyze.
GOLDEN_RECORDS = [
    {
        "c_of_o_id": "C-OF-O-LAG-001", "plot_number": 15, "block_number": 10, "area_name": "Lekki Scheme 1", "state": "Lagos",
        "owner_name": "RealVest Nigeria PLC", "date_registered": "2024-01-15", "status": "Under Dispute"
    },
    {
        "c_of_o_id": "C-OF-O-AWK-001", "plot_number": 7, "block_number": 5, "area_name": "Udoka Housing Estate", "state": "Anambra",
        "owner_name": "Anambra Digital Hub Ltd.", "date_registered": "2024-02-20", "status": "Verified"
    },
    {
        "c_of_o_id": "C-OF-O-ENU-001", "plot_number": 22, "block_number": 3, "area_name": "Independence Layout", "state": "Enugu",
        "owner_name": "Eastern Minerals Corp.", "date_registered": "2023-11-30", "status": "Pledged as Collateral"
    },
    {
        "c_of_o_id": "C-OF-O-LAG-002", "plot_number": 101, "block_number": 2, "area_name": "Apapa", "state": "Lagos",
        "owner_name": "Global Shipping Inc.", "date_registered": "2022-05-10", "status": "Revoked"
    },
    {
        "c_of_o_id": "C-OF-O-AWK-002", "plot_number": 34, "block_number": 12, "area_name": "Agu-Awka", "state": "Anambra",
        "owner_name": "The Okeke Family Trust", "date_registered": "2021-08-19", "status": "Verified"
    }
]

def generate_land_registry_csv():
    """
    Generates a mock Nigerian Land Registry CSV file with embedded golden records.
    """
    print("--- VERA AI | SPRINT 1, TASK 1.1: GENERATING LAND REGISTRY CSV ---")

    # Initialize the Faker library for generating realistic fake data.
    # 'en_NG' locale can provide more region-specific names if available.
    fake = Faker('en_NG')

    # Create the output directory if it doesn't already exist.
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
        print(f"Created output directory: '{OUTPUT_FOLDER}/'")

    # --- Generate "Noise" Records ---
    # These are the random records that will make up the bulk of the file.
    noise_records = []
    num_noise_rows = NUM_TOTAL_ROWS - len(GOLDEN_RECORDS)
    
    # Define locations for random data generation to make it more realistic.
    locations = {
        'Lagos': ['Ikoyi', 'Victoria Island', 'Ikeja GRA', 'Surulere'],
        'Anambra': ['Onitsha GRA', 'Nnewi', 'Amawbia', 'Enugu-Ukwu'],
        'Enugu': ['New Haven', 'Trans-Ekulu', 'GRA', 'Uwani']
    }
    # This distribution ensures that "Verified" is the most common status.
    status_choices = ['Verified'] * 99 + ['Under Dispute', 'Revoked', 'Pledged as Collateral']

    print(f"Generating {num_noise_rows} random 'noise' records...")
    for _ in range(num_noise_rows):
        state = random.choice(list(locations.keys()))
        record = {
            'c_of_o_id': f'C-OF-O-{fake.uuid4()[:8].upper()}',
            'plot_number': fake.random_int(min=1, max=200),
            'block_number': fake.random_int(min=1, max=50),
            'area_name': random.choice(locations[state]),
            'state': state,
            'owner_name': fake.name(),
            'date_registered': fake.date_between(start_date='-15y', end_date='-1y').strftime('%Y-%m-%d'),
            'status': random.choice(status_choices)
        }
        noise_records.append(record)
    
    # --- Combine and Shuffle Data ---
    print("Combining 'noise' records with 5 'golden' records...")
    all_records = noise_records + GOLDEN_RECORDS
    
    # Shuffling is crucial! This hides our golden records within the dataset,
    # forcing the AI to perform a real search.
    random.shuffle(all_records)

    # --- Create and Save the DataFrame ---
    # Use pandas to convert our list of dictionaries into a structured DataFrame.
    df = pd.DataFrame(all_records)
    
    # Define the final path for the output file.
    output_path = os.path.join(OUTPUT_FOLDER, OUTPUT_FILENAME)
    
    # Save the DataFrame to a CSV file. `index=False` prevents pandas
    # from writing an extra row index column.
    df.to_csv(output_path, index=False)

    print(f"\nSUCCESS: '{output_path}' created successfully with {len(df)} rows.")
    print("--- TASK 1.1 COMPLETE ---")

# This block allows the script to be run directly from the command line.
if __name__ == "__main__":
    generate_land_registry_csv()
