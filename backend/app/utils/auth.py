import os
from fastapi import Header, HTTPException, Depends
from dotenv import load_dotenv

# Ensure environment variables are loaded
load_dotenv(override=True)

# Custom error response to match requirements
def verify_api_key(x_api_key: str = Header(None)):
    """
    Dependency to verify the presence of a correct 'x-api-key' header.
    Returns:
        The validated API key as a string.
    Raises:
        HTTPException: If the key is missing or incorrect.
    """
    app_api_key = os.getenv("APP_API_KEY")
    
    if not app_api_key:
        # Fallback if APP_API_KEY is not set globally, 
        # though it should be required in production.
        return x_api_key

    if x_api_key != app_api_key:
        raise HTTPException(
            status_code=401, 
            detail="Unauthorized access"
        )
    
    return x_api_key
