# =================================================================
# Vira Engine - Gemini AI Integration Module
# =================================================================
# Purpose: This module handles the integration with Google's Gemini AI.
# It configures the API connection and provides model access for the
# property risk analysis system.
# =================================================================

import os
from dotenv import load_dotenv  # For secure environment variable handling
import google.generativeai as genai

# =================================================================
# Environment Configuration
# =================================================================
# We use python-dotenv to load environment variables from .env file
# This is a security best practice to avoid hardcoding API keys
# The .env file should never be committed to version control
load_dotenv()

# =================================================================
# Gemini API Configuration
# =================================================================
# Get API key from environment variables
# If not found, raise an error to ensure proper setup
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

# Configure the Gemini AI client with our API key
genai.configure(api_key=api_key)

# =================================================================
# Model Availability Check
# =================================================================
# List all available models to:
# 1. Verify API connection is working
# 2. Show which models we can use
# 3. Help in debugging if the needed model isn't available
for m in genai.list_models():
    print(m.name)
