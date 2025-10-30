# VERA AI - SPRINT 3, TASK 3.3: FULL API INTEGRATION
# This script integrates the AI analysis and ZK simulation into the FastAPI endpoint.

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware # Import CORS middleware
import uvicorn
import traceback
from datetime import datetime
import pandas as pd
import json

# --- Import our custom modules ---
# We import the functions we built in the previous sprints.
from main import perform_asset_analysis, get_asset_data, run_llm_investigation
from zk_proof_simulator import generate_mock_zk_proof

# --- Project Information ---
DESCRIPTION = """
Vera AI: The AI-Powered Risk Oracle for Real-World Assets. 🛡️

This API provides real-time risk analysis for tokenized real-world assets.
You can request an analysis for a specific asset token ID, and Vera AI will
perform a deep analysis of off-chain data to provide a risk assessment and a
verifiable proof hash.
"""

# --- Initialize the FastAPI App ---
app = FastAPI(
    title="Vera AI Oracle",
    description=DESCRIPTION,
    version="1.0.0", # Version bump to 1.0.0 for our first complete version
    contact={
        "name": "Vera AI Development Team",
        "email": "dev@vera-ai.example.com",
    },
)

# --- Add CORS Middleware ---
# This is crucial for allowing your frontend developer to call this API
# from a web browser hosted on a different domain (e.g., localhost:3000).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


# ========================================
# --- API Endpoints ---
# ========================================

# --- Endpoint 1: Root / Status Check ---
@app.get("/", tags=["Status"])
async def root():
    """
    Root endpoint to check the status of the API.
    Returns a welcome message confirming the server is running.
    """
    print("[API] Status check endpoint was hit.")
    return {"message": "Welcome to the Vera AI Oracle. The API is running."}


# --- Endpoint 2: The Main Analysis Endpoint (NOW FULLY IMPLEMENTED) ---
@app.get("/analyze/{token_id}", tags=["Analysis"])
async def analyze_asset(token_id: str):
    """
    Triggers the full, real-time risk analysis for a given asset token ID.
    This process involves:
    1. Data Ingestion
    2. Land Registry Verification
    3. Public News & Gazette Scan
    4. AI-Powered Document Review
    5. Proof Simulation
    """
    print(f"[API] Received analysis request for token_id: {token_id}")
    evidence_summary = []
    final_report = {
        "token_id": token_id,
        "status": "Failed",
        "risk_assessment": {"potential_risk_type": "Analysis Error", "summary": "Analysis could not be completed."},
        "evidence_summary": evidence_summary,
        "last_analyzed": datetime.utcnow().isoformat() + "Z"
    }
    try:
        # Step 1: Ingest Data
        asset_data = get_asset_data(token_id)
        if not asset_data:
            final_report["details"] = f"Asset token '{token_id}' not found in metadata registry."
            evidence_summary.append({
                "step": "Initial Data Ingestion",
                "result": "Failure",
                "details": f"Could not find metadata for token '{token_id}'."
            })
            raise HTTPException(status_code=404, detail=final_report["details"])
        # Step 2a: Land Registry Verification
        try:
            registry_df = pd.read_csv(asset_data['registry_path'])
            asset_row = registry_df[registry_df['c_of_o_id'] == asset_data['registry_key']]
            if not asset_row.empty:
                status = asset_row.iloc[0]['status']
                owner_name = asset_row.iloc[0]['owner_name']
                evidence_summary.append({
                    "step": "Land Registry Verification",
                    "result": "Success" if status == "Verified" else "Failure",
                    "details": f"Asset with C-of-O ID '{asset_data['registry_key']}' found. Status is '{status}'."
                })
            else:
                raise FileNotFoundError("Asset not found in registry.")
        except Exception as e:
            evidence_summary.append({
                "step": "Land Registry Verification",
                "result": "Failure",
                "details": f"Could not verify asset in land registry: {e}"
            })
            raise HTTPException(status_code=404, detail=f"Could not verify asset in land registry: {e}")
        # Step 2b: Public News & Gazette Scan
        try:
            with open(asset_data['news_path'], 'r') as f:
                news_alerts = json.load(f)
            relevant_news = [alert for alert in news_alerts if owner_name and owner_name in alert.get('summary', '')]
            if relevant_news:
                headlines = [news.get('headline', 'N/A') for news in relevant_news]
                evidence_summary.append({
                    "step": "Public News & Gazette Scan",
                    "result": "Failure",
                    "details": f"Found {len(relevant_news)} adverse news record(s) concerning owner '{owner_name}'. Headlines: {', '.join(headlines)}"
                })
            else:
                evidence_summary.append({
                    "step": "Public News & Gazette Scan",
                    "result": "Success",
                    "details": f"Scanned public records. No adverse news found concerning owner '{owner_name}'."
                })
        except Exception as e:
            evidence_summary.append({
                "step": "Public News & Gazette Scan",
                "result": "Failure",
                "details": f"Could not scan news records: {e}"
            })
            raise HTTPException(status_code=500, detail=f"Could not scan news records: {e}")
        # Step 3: AI-Powered Document Review
        llm_result = run_llm_investigation(token_id)
        if llm_result and "potential_risk_type" in llm_result:
            risk_type = llm_result["potential_risk_type"]
            is_risk_found = risk_type != "No Risk Found"
            evidence_summary.append({
                "step": "Legal Document Review (AI)",
                "result": "Success" if not is_risk_found else "Failure",
                "details": f"AI review of legal documents concluded: '{risk_type}'."
            })
            final_report["status"] = "Success"
            final_report["risk_assessment"] = {
                "potential_risk_type": risk_type,
                "summary": f"Comprehensive analysis completed. AI model identified a risk of '{risk_type}'." if is_risk_found else "Comprehensive analysis of all data sources found no indicators of title dispute, financial encumbrance, or government revocation."
            }
        else:
            evidence_summary.append({
                "step": "Legal Document Review (AI)",
                "result": "Failure",
                "details": "AI model returned an unexpected or empty result."
            })
            final_report["status"] = "Partial Success"
            final_report["risk_assessment"]["summary"] = "Analysis was inconclusive due to an AI model error."
        # Step 4: Proof Simulation
        mock_proof = generate_mock_zk_proof(final_report)
        final_response = {
            "analysis_report": final_report,
            "onchain_proof_simulation": mock_proof
        }
        print(f"[API] Successfully completed analysis for {token_id}. Returning full response.")
        return final_response
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"[API] CRITICAL ERROR in /analyze endpoint: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"An unexpected internal server error occurred: {str(e)}")


# ========================================
# --- Main Execution Block ---
# ========================================
if __name__ == "__main__":
    print("--- Starting Vera AI Server ---")
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
