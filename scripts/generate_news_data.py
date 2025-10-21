# SPRINT 1, TASK 1.2 (ENHANCED)
# VERA AI - DATA GENERATION SCRIPT
# This script generates the mock news JSON file with 4 distinct golden alerts.

import json
from faker import Faker
import random
import os
from datetime import datetime

# --- Configuration ---
NUM_TOTAL_ALERTS = 500
OUTPUT_FOLDER = "nigeria_demo_data"
OUTPUT_FILENAME = "Nigerian_Gazette_Alerts.json"

# --- Golden Alerts Definition (Now a list of 4 distinct scenarios) ---
GOLDEN_ALERTS = [
    # 1. Litigation Alert for NGA-LAG-001
    {
        'alert_id': 'NG-ALERT-DEMO-001', 'date': '2025-10-21', 'source': 'Lagos State High Court', 'category': 'Legal Notice',
        'headline': 'Public Notice of Litigation regarding Plot 15, Lekki Scheme 1',
        'summary': 'A lawsuit has been filed by The Estate of Chief Oluwole against RealVest Nigeria PLC concerning the rightful title of property located at Plot 15, Block 10, Lekki Peninsula Scheme 1. The case file is #LHC/CV/2025/987.'
    },
    # 2. Collateral Alert for NGA-ENU-001
    {
        'alert_id': 'NG-ALERT-DEMO-002', 'date': '2025-09-15', 'source': 'Business Day NG', 'category': 'Corporate Finance',
        'headline': 'Eastern Minerals Corp. Secures N2.5Billion Loan from FirstBank',
        'summary': 'In a recent filing, Eastern Minerals Corp. announced it has secured a N2.5B loan facility from FirstBank PLC. The loan is collateralized by several corporate assets, including its real estate holdings in Independence Layout, Enugu, specifically the property with C-of-O ID C-OF-O-ENU-001.'
    },
    # 3. Revocation Alert for NGA-LAG-002
    {
        'alert_id': 'NG-ALERT-DEMO-003', 'date': '2025-08-01', 'source': 'Lagos State Official Gazette', 'category': 'Government Notice',
        'headline': 'Notice of Revocation of Right of Occupancy for Apapa Industrial Zone',
        'summary': 'The Lagos State Government hereby gives notice of the immediate revocation of the Right of Occupancy for properties designated for the new port expansion project. This includes the property owned by Global Shipping Inc. at Plot 101, Block 2, Apapa, under C-of-O ID C-OF-O-LAG-002, for overriding public interest.'
    },
    # 4. Positive Verification Alert for NGA-AWK-001
    {
        'alert_id': 'NG-ALERT-DEMO-004', 'date': '2025-07-20', 'source': 'Anambra State Investment Promotion Agency', 'category': 'Economic Development',
        'headline': 'Anambra Digital Hub Project Receives Final Approval',
        'summary': 'The proposed Anambra Digital Hub, a project led by Anambra Digital Hub Ltd., has received final government approval. The site, located at Udoka Housing Estate on the property with C-of-O ID C-OF-O-AWK-001, has been fully verified and cleared for development to begin in Q4.'
    }
]

def generate_enhanced_gazette_alerts_json():
    """
    Generates a mock JSON file with 4 distinct golden alerts embedded.
    """
    print("--- VERA AI | SPRINT 1, TASK 1.2 (ENHANCED): GENERATING NEWS & ALERTS JSON ---")

    fake = Faker()
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
        print(f"Created output directory: '{OUTPUT_FOLDER}/'")

    # Adjust the number of noise alerts to make space for our 4 golden alerts.
    num_noise_alerts = NUM_TOTAL_ALERTS - len(GOLDEN_ALERTS)
    noise_alerts = []
    
    print(f"Generating {num_noise_alerts} random 'noise' alerts...")
    for _ in range(num_noise_alerts):
        noise_alerts.append({
            'alert_id': f'NG-ALERT-{fake.random_number(digits=6)}',
            'date': fake.date_this_year().strftime('%Y-%m-%d'),
            'source': random.choice(['Channels TV', 'NTA News', 'The Punch', 'Federal Ministry of Information']),
            'category': random.choice(['Infrastructure', 'Politics', 'Business', 'Sports', 'Entertainment']),
            'headline': fake.bs().title(),
            'summary': fake.paragraph(nb_sentences=2)
        })

    print(f"Combining 'noise' alerts with the {len(GOLDEN_ALERTS)} 'golden' alerts...")
    all_alerts = noise_alerts + GOLDEN_ALERTS
    random.shuffle(all_alerts)

    output_path = os.path.join(OUTPUT_FOLDER, OUTPUT_FILENAME)
    with open(output_path, 'w') as f:
        json.dump(all_alerts, f, indent=2)

    print(f"\nSUCCESS: '{output_path}' created successfully with {len(all_alerts)} entries.")
    print("--- TASK 1.2 (ENHANCED) COMPLETE ---")

if __name__ == "__main__":
    generate_enhanced_gazette_alerts_json()
