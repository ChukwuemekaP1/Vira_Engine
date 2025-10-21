# VERA AI - SPRINT 3, TASK 3.2: FASTAPI ENDPOINT SETUP
# This script creates the main web server for the Vera AI backend.

from fastapi import FastAPI, HTTPException
import uvicorn # The server that runs our FastAPI application

# --- Project Information ---
# This information will be used in the automatic API documentation.
DESCRIPTION = """
Vera AI: The AI-Powered Risk Oracle for Real-World Assets. 🛡️

This API provides real-time risk analysis for tokenized real-world assets.
You can request an analysis for a specific asset token ID, and Vera AI will
perform a deep analysis of off-chain data to provide a risk assessment.
"""

# --- Initialize the FastAPI App ---
# We provide metadata here for the auto-generated documentation.
app = FastAPI(
    title="Vera AI Oracle",
    description=DESCRIPTION,
    version="0.1.0",
    contact={
        "name": "Vera AI Development Team",
      
    },
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


# --- Endpoint 2: The Main Analysis Endpoint (Placeholder) ---
@app.get("/analyze/{token_id}", tags=["Analysis"])
async def analyze_asset(token_id: str):
    """
    **Placeholder:** This endpoint will trigger the full asset analysis.
    
    For now, it simply confirms the token_id it received. In the next task,
    we will integrate our full AI and ZK-proof logic here.
    
    - **token_id**: The unique identifier for the asset to be analyzed (e.g., "NGA-LAG-001").
    """
    print(f"[API] Analysis endpoint was hit for token_id: {token_id}")
    
    # For now, we just return a simple confirmation.
    # In the next step, we will replace this with a call to our analysis functions.
    return {
        "message": "Analysis request received. Logic not yet implemented.",
        "token_id_received": token_id
    }


# ========================================
# --- Main Execution Block (for direct execution) ---
# ========================================
# This allows us to run the server directly by executing `python api.py`
if __name__ == "__main__":
    print("--- Starting Vera AI Server ---")
    # Uvicorn will run the 'app' instance in this file ('api:app')
    # host="0.0.0.0" makes it accessible on your local network
    # reload=True automatically restarts the server when you save changes
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
