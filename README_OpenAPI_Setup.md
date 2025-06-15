# OpenAPI Tool Setup for Image Generation

This guide explains how to set up the OpenAI Images API integration using Azure AI Agents' OpenAPI tool functionality.

## Overview

The implementation now uses `OpenApiTool` instead of `FunctionTool` to integrate directly with the OpenAI Images API. This approach is more robust and follows Azure AI Agents best practices for external API integration.

## Setup Steps

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Required Environment Variables

Add these to your `.env` file:

```bash
# Existing variables
PROJECT_CONNECTION_STRING=your_project_connection_string
OPEN_API_KEY_FOR_IMAGES=your_openai_api_key

# Additional variables for connection creation
AZURE_SUBSCRIPTION_ID=your_subscription_id
AZURE_RESOURCE_GROUP=your_resource_group_name
AZURE_AI_PROJECT_NAME=your_ai_project_name
```

### 3. Create OpenAI Connection in Azure AI Foundry

#### Option A: Automatic Setup (Recommended)

Run the helper script to create the connection automatically:

```bash
python3 create_connection.py
```

#### Option B: Manual Setup

You need to create a connection in Azure AI Foundry that stores your OpenAI API key:

1. Go to the [Azure AI Foundry portal](https://ai.azure.com)
2. Navigate to your project
3. Go to **Settings** → **Connections**
4. Click **+ New connection**
5. Select **Custom keys**
6. Fill in the details:
   - **Name**: `openai_images_connection` (or update the `OPENAI_CONNECTION_ID` env var)
   - **Target**: `https://api.openai.com/v1`
   - **Authentication**: Custom Keys
   - **Key**: Your OpenAI API key (from `OPEN_API_KEY_FOR_IMAGES`)

### 3. Update Environment Variables

Add the connection ID to your `.env` file:

```bash
# Existing variables
PROJECT_CONNECTION_STRING="your_azure_ai_project_connection_string"
OPEN_API_KEY_FOR_IMAGES="your_openai_api_key"

# New variable for OpenAPI tool
OPENAI_CONNECTION_ID="openai_images_connection"
```

### 4. Run the Application

```bash
python3 multi-agent-demo.py
```

## How It Works

1. **OpenAPI Specification**: The `openai_images_spec.json` file contains the OpenAI Images API specification
2. **Authentication**: Uses Azure AI connection-based authentication with your OpenAI API key
3. **Tool Integration**: The `create_image` tool is available to the marketing campaign orchestrator
4. **Workflow**: 
   - Image generator agent provides visual concepts
   - Orchestrator calls the `create_image` tool with specific prompts
   - OpenAI generates images via the API
   - Results are included in the campaign output

## OpenAPI Specification

The `openai_images_spec.json` file defines:
- **Endpoint**: `/images/generations` (POST)
- **Parameters**: prompt, model, size, quality, style, etc.
- **Authentication**: Bearer token (handled by Azure AI connection)
- **Response**: Image URLs or base64 data

## Benefits of OpenAPI Tool Approach

1. **Direct API Integration**: No need for wrapper functions
2. **Proper Authentication**: Secure handling via Azure AI connections
3. **Standardized**: Follows OpenAPI standards
4. **Maintainable**: Easy to update API parameters
5. **Scalable**: Can be extended to other OpenAI endpoints

## Troubleshooting

### Connection Issues
- Verify the connection name matches `OPENAI_CONNECTION_ID`
- Check that the OpenAI API key is valid
- Ensure the connection target URL is correct

### API Errors
- Check OpenAI API key permissions and quota
- Verify the OpenAPI specification is valid
- Review Azure AI Foundry logs for detailed error messages

### Tool Not Called
- Check orchestrator instructions reference the correct tool name (`create_image`)
- Verify the tool description is clear for the LLM
- Ensure the image_generator agent is providing suitable visual concepts

## Reference

- [Azure AI Agents OpenAPI Tools Documentation](https://learn.microsoft.com/en-us/azure/ai-services/agents/how-to/tools/openapi-spec-samples?pivots=python)
- [OpenAI Images API Documentation](https://platform.openai.com/docs/api-reference/images) 