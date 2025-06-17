#!/usr/bin/env python3
"""
Helper script to create OpenAI API connection in Azure AI Foundry.
Run this script before running the main demo to set up the required connection.
"""

import os
import requests
import json
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.core.credentials import AccessToken

load_dotenv()

def get_azure_token():
    """Get Azure access token for Azure AI Foundry API calls"""
    credential = DefaultAzureCredential()
    token = credential.get_token("https://management.azure.com/.default")
    return token.token

def create_openai_connection():
    """Create a custom key connection for OpenAI API"""
    
    # Get required environment variables
    subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
    resource_group = os.getenv("AZURE_RESOURCE_GROUP")
    workspace_name = os.getenv("AZURE_AI_PROJECT_NAME")  # Or AZURE_WORKSPACE_NAME
    api_key = os.getenv("OPEN_API_KEY_FOR_IMAGES")
    
    if not all([subscription_id, resource_group, workspace_name, api_key]):
        print("Missing required environment variables:")
        print("- AZURE_SUBSCRIPTION_ID")
        print("- AZURE_RESOURCE_GROUP") 
        print("- AZURE_AI_PROJECT_NAME (or AZURE_WORKSPACE_NAME)")
        print("- OPEN_API_KEY_FOR_IMAGES")
        return False
    
    # Azure AI Foundry connection API endpoint
    connection_name = "openai_images_connection"
    url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.MachineLearningServices/workspaces/{workspace_name}/connections/{connection_name}"
    
    # Connection payload
    payload = {
        "properties": {
            "category": "CustomKeys",
            "authType": "CustomKeys",
            "credentials": {
                "keys": {
                    "Authorization": f"Bearer {api_key}"
                }
            },
            "target": "https://api.openai.com/v1"
        }
    }
    
    # Headers
    token = get_azure_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Make the API call
    try:
        response = requests.put(
            url,
            json=payload,
            headers=headers,
            params={"api-version": "2024-04-01"}
        )
        
        if response.status_code in [200, 201]:
            print(f"✅ Successfully created connection: {connection_name}")
            return True
        else:
            print(f"❌ Failed to create connection. Status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating connection: {str(e)}")
        return False

def main():
    print("🔧 Creating OpenAI API connection for Azure AI Foundry...")
    print("-" * 50)
    
    success = create_openai_connection()
    
    if success:
        print("\n✅ Connection created successfully!")
        print("You can now run the multi-agent demo:")
        print("python3 multi-agent-demo.py")
    else:
        print("\n❌ Failed to create connection.")
        print("\nManual setup instructions:")
        print("1. Go to Azure AI Foundry portal (ai.azure.com)")
        print("2. Navigate to your project")
        print("3. Go to Settings → Connections")
        print("4. Click '+ New connection'")
        print("5. Select 'Custom keys'")
        print("6. Set:")
        print("   - Connection name: openai_images_connection")
        print("   - Key name: Authorization")
        print(f"   - Key value: Bearer {os.getenv('OPEN_API_KEY_FOR_IMAGES', 'YOUR_API_KEY')}")

if __name__ == "__main__":
    main() 