# File: setup_project_data.py
import pandas as pd
import json
import os

# --- 1. Define Directory and File Paths ---
# This variable holds the name of the folder for all our data.
DATA_DIR = "nigeria_demo_data"
CSV_PATH = os.path.join(DATA_DIR, "Nigerian_Land_Registry_Mock.csv")
JSON_PATH = os.path.join(DATA_DIR, "Nigerian_Gazette_Alerts.json")

# Create the directory if it doesn't exist to prevent errors.
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
    print(f"Created directory: {DATA_DIR}")

# --- 2. Create the Land Registry CSV File ---
# This dictionary contains the complete data for 10 assets.
registry_data = {
    'Certificate_of_Occupancy_ID': [
        'C-OF-O-LAG-12345', 'C-OF-O-ABJ-67890', 'C-OF-O-PHC-11223', 'C-OF-O-KAD-44556', 'C-OF-O-ENu-77889',
        'C-OF-O-LAG-10111', 'C-OF-O-AWK-20222', 'C-OF-O-LAG-30333', 'C-OF-O-AWK-40444', 'C-OF-O-LAG-50555'
    ],
    'Plot_Number': [10, 5, 15, 20, 25, 42, 18, 8, 25, 12],
    'Block_Number': [4, 2, 6, 8, 10, 15, 7, 22, 3, 9],
    'Street': [
        'Ademola Adetokunbo Crescent', 'Shehu Shagari Way', 'Trans-Amadi Industrial Layout', 'Ali Akilu Road', 'Ogui Road',
        'Bourdillon Road', 'Zik Avenue', 'Glover Road', 'Regina Caeli Road', 'Alexander Avenue'
    ],
    'LGA': ['Victoria Island', 'Maitama', 'Port Harcourt', 'Kaduna', 'Enugu', 'Ikoyi', 'Awka', 'Ikoyi', 'Awka', 'Ikoyi'],
    'State': ['Lagos', 'FCT', 'Rivers', 'Kaduna', 'Enugu', 'Lagos', 'Anambra', 'Lagos', 'Anambra', 'Lagos'],
    'Owner': [
        'Femi Adebayo', 'Aisha Buhari', 'Ngozi Okoro', 'Musa Yaradua', 'Chinedu Okafor',
        'Ngozi Okonjo-Iweala', 'Chukwuma Soludo', 'Aliko Dangote', 'Chimamanda Adichie', 'Herbert Wigwe'
    ],
    'Registration_Date': [
        '2020-05-10', '2018-11-22', '2021-01-15', '2019-03-30', '2022-07-19',
        '2023-02-15', '2022-11-20', '2024-03-10', '2023-08-01', '2022-09-05'
    ],
    'Status': [
        'Verified', 'Verified', 'Under Review', 'Revoked', 'Verified',
        'Verified', 'Verified', 'Under Review', 'Verified', 'Revoked'
    ],
    # This 'Token_ID' column is CRUCIAL for linking the CSV to the API endpoint.
    'Token_ID': [
        'NGA-LAG-001', 'NGA-ABJ-002', 'NGA-PHC-003', 'NGA-KAD-004', 'NGA-ENU-005',
        'NGA-LAG-006', 'NGA-AWK-007', 'NGA-LAG-008', 'NGA-AWK-009', 'NGA-LAG-010'
    ]
}
registry_df = pd.DataFrame(registry_data)
registry_df.to_csv(CSV_PATH, index=False)
print(f"Successfully created: {CSV_PATH}")


# --- 3. Create the Gazette Alerts JSON File ---
gazette_alerts = [
    {"alert_id": "NG-ALERT-001", "token_id": "NGA-LAG-001", "date": "2023-10-28", "source": "Lagos State Gazette", "category": "Government Notice", "headline": "Land Verification Exercise", "summary": "Verification of title documents..."},
    {"alert_id": "NG-ALERT-002", "token_id": "NGA-PHC-003", "date": "2023-09-15", "source": "Rivers State Property Chronicle", "category": "Dispute Alert", "headline": "Ownership Tussle on Trans-Amadi Property", "summary": "A legal dispute has been filed..."},
    {"alert_id": "NG-ALERT-003", "token_id": "NGA-KAD-004", "date": "2022-01-20", "source": "Kaduna State Government", "category": "Revocation of Title", "headline": "Revocation of Right of Occupancy", "summary": "The Certificate of Occupancy... has been revoked..."},
    {"alert_id": "NG-ALERT-2023-015", "token_id": "NGA-LAG-006", "date": "2023-03-01", "source": "Lagos State Gazette", "category": "Government Notice", "headline": "Verification of Title on Bourdillon Road", "summary": "Title C-OF-O-LAG-10111... has been successfully verified..."},
    {"alert_id": "NG-ALERT-2022-089", "token_id": "NGA-AWK-007", "date": "2022-12-05", "source": "Anambra State Gazette", "category": "Government Notice", "headline": "New Duplex Registration on Zik Avenue", "summary": "A new duplex property... has been registered..."},
    {"alert_id": "NG-ALERT-2024-032", "token_id": "NGA-LAG-008", "date": "2024-04-02", "source": "Federal Land Registry", "category": "Dispute Alert", "headline": "Ownership Dispute on Glover Road Property", "summary": "A legal challenge has been filed..."},
    {"alert_id": "NG-ALERT-2023-112", "token_id": "NGA-AWK-009", "date": "2023-09-15", "source": "Anambra State Ministry of Lands", "category": "Land Use Charge Update", "headline": "Land Use Charge Paid for Regina Caeli Road Property", "summary": "The annual land use charge... has been paid..."},
    {"alert_id": "NG-ALERT-2023-045", "token_id": "NGA-LAG-010", "date": "2023-05-20", "source": "Lagos State Government", "category": "Revocation of Title", "headline": "Revocation of Certificate of Occupancy on Alexander Avenue", "summary": "The Certificate of Occupancy... has been revoked..."}
]
with open(JSON_PATH, 'w') as f:
    json.dump(gazette_alerts, f, indent=2)
print(f"Successfully created: {JSON_PATH}")


# --- 4. Create Individual Asset Document (.txt) Files ---
# The filenames (e.g., "NGA-LAG-001.txt") must match the Token_ID.
asset_documents = {
    "NGA-LAG-001.txt": "DEED OF ASSIGNMENT for C-OF-O-LAG-12345. Assignee: Femi Adebayo.",
    "NGA-ABJ-002.txt": "DEED OF ASSIGNMENT for C-OF-O-ABJ-67890. Assignee: Aisha Buhari.",
    "NGA-PHC-003.txt": "DEED OF ASSIGNMENT for C-OF-O-PHC-11223. Note: Title is currently under legal review.",
    "NGA-KAD-004.txt": "DEED OF ASSIGNMENT for C-OF-O-KAD-44556. WARNING: This title has been officially revoked.",
    "NGA-ENU-005.txt": "DEED OF ASSIGNMENT for C-OF-O-ENu-77889. Assignee: Chinedu Okafor.",
    "NGA-LAG-006.txt": "DEED OF ASSIGNMENT for C-OF-O-LAG-10111. Assignee: Ngozi Okonjo-Iweala.",
    "NGA-AWK-007.txt": "DEED OF ASSIGNMENT for C-OF-O-AWK-20222. Assignee: Chukwuma Soludo.",
    "NGA-LAG-008.txt": "DEED OF ASSIGNMENT for C-OF-O-LAG-30333. Note: A third-party claim has been noted.",
    "NGA-AWK-009.txt": "DEED OF ASSIGNMENT for C-OF-O-AWK-40444. Assignee: Chimamanda Adichie.",
    "NGA-LAG-010.txt": "DEED OF ASSIGNMENT for C-OF-O-LAG-50555. This title has been marked as REVOKED."
}

for filename, content in asset_documents.items():
    file_path = os.path.join(DATA_DIR, filename)
    with open(file_path, 'w') as f:
        f.write(content)
    print(f"Successfully created: {file_path}")

print("\nProject data setup complete!")

