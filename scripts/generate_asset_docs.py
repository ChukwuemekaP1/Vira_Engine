# SPRINT 1, TASK 1.3 (REVISED)
# VERA AI - DATA GENERATION SCRIPT
# This script generates the individual asset documentation with varied dates.

import json
import os

# --- Configuration ---
OUTPUT_FOLDER = "nigeria_demo_data"
METADATA_SUBFOLDER = "metadata"

# --- Asset Profiles Definition (with varied dates) ---
# This list now has different 'date_registered' values for each asset.
ASSET_PROFILES = [
    {
        "token_id": "NGA-LAG-001", "owner": "RealVest Nigeria PLC", "plot": 15, "block": 10, "area": "Lekki Scheme 1", "state": "Lagos",
        "c_of_o": "C-OF-O-LAG-001", "status": "Under Dispute", "deed_notes": "Assignee is a major property development company.", "date_registered": "2024-01-15"
    },
    {
        "token_id": "NGA-AWK-001", "owner": "Anambra Digital Hub Ltd.", "plot": 7, "block": 5, "area": "Udoka Housing Estate", "state": "Anambra",
        "c_of_o": "C-OF-O-AWK-001", "status": "Verified", "deed_notes": "Property designated for a new technology park.", "date_registered": "2024-02-20"
    },
    {
        "token_id": "NGA-ENU-001", "owner": "Eastern Minerals Corp.", "plot": 22, "block": 3, "area": "Independence Layout", "state": "Enugu",
        "c_of_o": "C-OF-O-ENU-001", "status": "Pledged as Collateral", "deed_notes": "Asset is pledged as collateral against a corporate loan with FirstBank PLC.", "date_registered": "2023-11-30"
    },
    {
        "token_id": "NGA-LAG-002", "owner": "Global Shipping Inc.", "plot": 101, "block": 2, "area": "Apapa", "state": "Lagos",
        "c_of_o": "C-OF-O-LAG-002", "status": "Revoked", "deed_notes": "Certificate of Occupancy was revoked by Lagos State Government notice.", "date_registered": "2022-05-10"
    },
    {
        "token_id": "NGA-AWK-002", "owner": "The Okeke Family Trust", "plot": 34, "block": 12, "area": "Agu-Awka", "state": "Anambra",
        "c_of_o": "C-OF-O-AWK-002", "status": "Verified", "deed_notes": "Property held in a multi-generational family trust.", "date_registered": "2021-08-19"
    }
]

def generate_asset_documentation_revised():
    """
    Generates all Deed of Assignment and Metadata files with varied dates.
    """
    print("--- VERA AI | SPRINT 1, TASK 1.3 (REVISED): GENERATING ASSET DOCUMENTATION ---")

    # --- Create Deed of Assignment Files ---
    print("\n[1/2] Generating Deed of Assignment (.txt) files with varied dates...")
    for profile in ASSET_PROFILES:
        file_name = f"{profile['token_id']}_Deed_of_Assignment.txt"
        file_path = os.path.join(OUTPUT_FOLDER, file_name)
        
        # --- THIS IS THE CHANGED LINE ---
        # The date is now dynamically pulled from the profile, not hardcoded.
        execution_date = profile['date_registered']
        
        content = f"""
*** DEED OF ASSIGNMENT (SUMMARY) ***

ASSET_TOKEN_ID: {profile['token_id']}
DATE_OF_EXECUTION: {execution_date}

PARTIES:
- ASSIGNOR (SELLER): Mr. John Doe (Simulated)
- ASSIGNEE (BUYER): {profile['owner']}

PROPERTY_DETAILS:
- DESCRIPTION: All that piece or parcel of land situated at Plot {profile['plot']}, Block {profile['block']}, {profile['area']}, {profile['state']} State, Nigeria.
- LAND_REGISTRY_ID: {profile['c_of_o']}

NOTES:
- {profile['deed_notes']}
"""
        with open(file_path, 'w') as f:
            f.write(content.strip())
        print(f"  - Created '{file_path}'")
    print("...Deed files complete.")

    # --- Create Metadata JSON Files ---
    # (No changes are needed in this section, but it's included for completeness)
    print("\n[2/2] Generating Metadata (.json) files...")
    metadata_path = os.path.join(OUTPUT_FOLDER, METADATA_SUBFOLDER)
    if not os.path.exists(metadata_path):
        os.makedirs(metadata_path)
        print(f"  - Created metadata subfolder: '{metadata_path}/'")

    for profile in ASSET_PROFILES:
        file_name = f"{profile['token_id']}.json"
        file_path = os.path.join(metadata_path, file_name)
        metadata_content = {
            "name": f"Vera AI Asset: {profile['token_id']}",
            "description": f"Tokenized asset representing property in {profile['area']}, {profile['state']}. Owned by {profile['owner']}.",
            "attributes": [
                {"trait_type": "Human-Readable ID", "value": profile['token_id']},
                {"trait_type": "Deed of Assignment Path", "value": os.path.join(OUTPUT_FOLDER, f"{profile['token_id']}_Deed_of_Assignment.txt")},
                {"trait_type": "Public News API Path", "value": os.path.join(OUTPUT_FOLDER, "Nigerian_Gazette_Alerts.json")},
                {"trait_type": "Land Registry File Path", "value": os.path.join(OUTPUT_FOLDER, "Nigerian_Land_Registry_Mock.csv")},
                {"trait_type": "Registry Search Key", "value": profile['c_of_o']}
            ]
        }
        with open(file_path, 'w') as f:
            json.dump(metadata_content, f, indent=2)
        print(f"  - Created '{file_path}'")
    print("...Metadata files complete.")
    
    print("\nSUCCESS: All asset documentation has been generated with realistic, varied dates.")
    print("--- TASK 1.3 (REVISED) COMPLETE ---")

if __name__ == "__main__":
    generate_asset_documentation_revised()
