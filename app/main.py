# =================================================================
# Vira Engine - Main Application Module
# =================================================================
# This is the core module of the Vira Engine that handles property
# risk analysis using Google's Gemini AI. It processes multiple data
# sources to identify potential risks in Nigerian real estate
# transactions.
#
# Key Features:
# - Multi-source data integration
# - AI-powered risk analysis
# - Structured output format
# - Error handling and logging
# =================================================================

import os
import json
import sys
import traceback
import google.generativeai as genai  # Gemini AI SDK for risk analysis
import pandas as pd  # For handling structured data

# ========================================
# CONFIGURATION
# ========================================
# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Get API key from environment variables
API_KEY = os.getenv('GEMINI_API_KEY')

# Define data folders relative to this script's location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_DIR, "..", "nigeria_demo_data")
METADATA_SUBFOLDER = "metadata"

# ========================================
# --- Task 2.1: Data Ingestion Module ---
# ========================================
def get_asset_data(token_id: str) -> dict:
    """Retrieves all necessary data paths and keys for a given asset token ID."""
    print(f"\n[Ingestion] Received request for token_id: '{token_id}'")
    metadata_filename = f"{token_id}.json"
    metadata_filepath = os.path.join(DATA_FOLDER, METADATA_SUBFOLDER, metadata_filename)
    if not os.path.exists(metadata_filepath):
        print(f"[Error] Metadata file not found at: '{metadata_filepath}'")
        return None
    try:
        with open(metadata_filepath, 'r') as f: metadata = json.load(f)
    except Exception: return None
    asset_info = {}
    for attribute in metadata.get("attributes", []):
        trait_type, value = attribute.get("trait_type"), attribute.get("value")
        if "Path" in trait_type: value = os.path.abspath(os.path.join(BASE_DIR, '..', value))
        if "Human-Readable ID" in trait_type: asset_info['token_id'] = value
        elif "Deed of Assignment Path" in trait_type: asset_info['deed_path'] = value
        elif "Public News API Path" in trait_type: asset_info['news_path'] = value
        elif "Land Registry File Path" in trait_type: asset_info['registry_path'] = value
        elif "Registry Search Key" in trait_type: asset_info['registry_key'] = value
    print("[Ingestion] Successfully extracted asset information.")
    return asset_info

# ========================================
# --- Task 2.2: AI Investigation Module (Using Gemini ChatSession) ---
# ========================================
def run_llm_investigation(token_id: str) -> dict:
    """Performs the AI Investigation using the Gemini ChatSession method."""
    print(f"\n[LLM Investigator] Starting investigation for token_id: '{token_id}'")
    
    # --- 1. Configure the API Key ---
    try:
        if not API_KEY or API_KEY == "YOUR_GOOGLE_API_KEY_HERE":
            print("[Error] Google API Key is missing. Please edit the script and paste your key.")
            return None
        genai.configure(api_key=API_KEY)
    except Exception as e:
        print(f"[Error] Failed to configure Gemini: {e}")
        traceback.print_exc()
        return None

    # --- 2. Get Asset Data ---
    asset_data = get_asset_data(token_id)
    if not asset_data: return None
    try:
        with open(asset_data['deed_path'], 'r') as f: deed_content = f.read()
        registry_df = pd.read_csv(asset_data['registry_path'])
        asset_row = registry_df[registry_df['c_of_o_id'] == asset_data['registry_key']]
        registry_content = asset_row.to_string() if not asset_row.empty else "Asset not found in registry."
        with open(asset_data['news_path'], 'r') as f: news_alerts = json.load(f)
        owner_name = asset_row.iloc[0]['owner_name'] if not asset_row.empty else ""
        relevant_news = [alert for alert in news_alerts if owner_name and owner_name in alert.get('summary', '')]
        news_content = json.dumps(relevant_news, indent=2) if relevant_news else "No relevant news found."
    except Exception:
        print(f"[Error] Failed to read source data files:")
        traceback.print_exc()
        return None

    # --- 3. Start a Chat Session with the AI ---
    try:
        print("[LLM Investigator] Initializing model and chat session...")
        # Use latest pro model
        model = genai.GenerativeModel('gemini-pro-latest')
        
        system_instruction = """
        You are "Vera," an AI Risk Analyst. Your only job is to analyze data and respond with a single, specific JSON object.
        The JSON object must have one key: "potential_risk_type".
        The possible values for this key are: "Title Dispute", "Financial Pledge", "Government Revocation", or "No Risk Found".
        Do not write any other text, explanation, or markdown. Only the JSON.
        """
        
        chat = model.start_chat(history=[
            {'role': 'user', 'parts': [system_instruction]},
            {'role': 'model', 'parts': ["Understood. I will only respond with the specified JSON object."]}
        ])

        # --- 4. Send the Data and Question as a Single Message ---
        prompt = f"""
        Analyze the following data for asset {token_id} and provide your risk assessment.

        --- DATASET 1: Deed of Assignment ---
        {deed_content}

        --- DATASET 2: Land Registry Record ---
        {registry_content}

        --- DATASET 3: Public News Alerts ---
        {news_content}
        """
        
        print("[LLM Investigator] Sending data to Gemini via chat...")
        response = chat.send_message(prompt)
        
        response_text = response.text.strip()
        print(f"[LLM Investigator] Received response: {response_text}")
        
        json_text = response_text.replace("```json", "").replace("```", "").strip()
        result = json.loads(json_text)
        return result

    except Exception:
        print("\n[Error] An error occurred during the Gemini chat session:")
        traceback.print_exc()
        return None

# ========================================
# --- Task 2.3: Create Core Analysis Function ---
# ========================================
def perform_asset_analysis(token_id: str) -> dict:
    """
    Orchestrates the full asset risk analysis for a given token_id.
    This function acts as the main entry point for the API.
    """
    print(f"\n[Core Analysis] Starting full analysis for token_id: '{token_id}'")
    
    # Start with a default "failed" report structure.
    # This ensures we always return a consistent format, even on error.
    final_report = {
        "token_id": token_id,
        "status": "Failed",
        "risk_assessment": {"potential_risk_type": "Analysis Error"},
        "details": "An unexpected error occurred during analysis."
    }

    try:
        # Call the LLM investigator function.
        llm_result = run_llm_investigation(token_id)
        
        # Check for errors returned from the investigator.
        if llm_result and "error" in llm_result:
            final_report["details"] = llm_result.get("message", "LLM investigation failed.")
            # Specifically check for the "Asset not found" error to set the status correctly.
            if llm_result.get("message") == "Asset not found.":
                final_report["status"] = "Not Found"
                final_report["risk_assessment"]["potential_risk_type"] = "Asset Not Found"
            print(f"[Core Analysis] LLM investigation failed: {final_report['details']}")

        # Check if the result from the LLM is valid and successful.
        elif llm_result and "potential_risk_type" in llm_result:
            # If successful, update the report.
            final_report["status"] = "Success"
            final_report["risk_assessment"] = llm_result
            final_report["details"] = "LLM investigation completed successfully."
        else:
            # Handle cases where the LLM might return an unexpected or empty response.
            final_report["status"] = "Partial Success"
            final_report["risk_assessment"] = {"potential_risk_type": "Unknown Risk"}
            final_report["details"] = "LLM investigation returned an unexpected or empty result."
            print(f"[Core Analysis] Warning: LLM result was unexpected: {llm_result}")

    except Exception as e:
        # Catch any critical errors during the process.
        final_report["details"] = f"Critical error during LLM investigation: {e}"
        print(f"[Core Analysis] Critical error: {e}")
        traceback.print_exc()

    print(f"[Core Analysis] Analysis complete for {token_id}.")
    return final_report

# ========================================
# MAIN EXECUTION
# ========================================
if __name__ == "__main__":
    print("\n" + "="*50)
    print("--- VERA AI | SPRINT 3: CORE ANALYSIS FUNCTION ---")
    print("="*50)
    
    test_token_id = "NGA-LAG-001"
    
    # Test the new perform_asset_analysis function
    analysis_result = perform_asset_analysis(test_token_id)
    
    print("\n[Result] Asset Analysis Complete.")
    print(json.dumps(analysis_result, indent=2))

    print("\n--- SPRINT 3 COMPLETE ---")
