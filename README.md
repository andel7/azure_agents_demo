# AI Tour 2025 - Multi-Agent Marketing Campaign Generator

A sophisticated multi-agent system built on Azure AI Agents that generates comprehensive marketing campaigns for TeraSky's cloud and DevOps solutions. This project demonstrates the power of orchestrated AI agents working together to create cohesive marketing strategies, content, and visual assets.

## 🚀 Overview

This project creates an intelligent marketing campaign generator using Azure AI Agents with multiple specialized agents:

- **Product Researcher**: Analyzes product features and capabilities
- **Audience Researcher**: Identifies target personas and market segments  
- **Campaign Strategist**: Develops comprehensive marketing strategies
- **Content Creator**: Generates marketing copy and messaging
- **Image Generator**: Creates visual concepts and actual images using DALL-E
- **QA Validator**: Ensures content quality and brand compliance

All agents are orchestrated by a central **Marketing Campaign Orchestrator** that coordinates the entire workflow and integrates OpenAI's image generation capabilities.

## 🏗️ Architecture

The system uses a multi-agent architecture with:

1. **Specialized Agents**: Each agent has a specific role and expertise area
2. **YAML Configuration**: Agent behaviors and instructions defined in configuration files
3. **OpenAPI Integration**: Direct integration with OpenAI Images API for visual content
4. **Azure AI Agents**: Leveraging Azure's agent framework for scalability and reliability

## 📁 Project Structure

```
AI_Tour_2025/
├── multi-agent-demo.py           # Main application entry point
├── cleanup.sh                    # Bash wrapper for cleanup automation
├── cleanup_automation.py         # Python cleanup automation script
├── agent_configs.yaml            # Configuration for specialized agents
├── orchestrator_config.yaml      # Configuration for main orchestrator
├── openai_images_spec.json       # OpenAPI specification for image generation
├── create_connection.py          # Helper for Azure AI connection setup
├── requirements.txt              # Python dependencies
├── README_OpenAPI_Setup.md       # Detailed OpenAPI setup guide
└── .env                          # Environment variables (create this)
```

## 🛠️ Installation & Setup

### 1. Prerequisites

- Python 3.8+
- Azure subscription with AI Services
- OpenAI API key
- Azure AI Project (Azure AI Foundry)

### 2. Clone and Install Dependencies

```bash
git clone <repository-url>
cd AI_Tour_2025
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file with the following variables:

```bash
# Azure AI Project Connection
PROJECT_CONNECTION_STRING="your_azure_ai_project_connection_string"

# OpenAI API Configuration
OPEN_API_KEY_FOR_IMAGES="your_openai_api_key"
OPENAI_CONNECTION_ID="openai_images_connection"

# Additional Azure Configuration (for connection creation)
AZURE_SUBSCRIPTION_ID="your_subscription_id"
AZURE_RESOURCE_GROUP="your_resource_group_name"
AZURE_AI_PROJECT_NAME="your_ai_project_name"
```

### 4. Azure AI Connection Setup

#### Option A: Automatic Setup
```bash
python3 create_connection.py
```

#### Option B: Manual Setup
1. Go to [Azure AI Foundry](https://ai.azure.com)
2. Navigate to your project → Settings → Connections
3. Create a new "Custom keys" connection:
   - **Name**: `openai_images_connection`
   - **Target**: `https://api.openai.com/v1`
   - **Authentication**: Custom Keys
   - **Key**: Your OpenAI API key

## 🎯 Usage

### Running the Demo

```bash
python3 multi-agent-demo.py
```

The application will:
1. Prompt you for a product name
2. Create and orchestrate multiple specialized agents
3. Generate a comprehensive marketing campaign
4. Create actual images using DALL-E
5. Provide a complete campaign package

### Example Workflow

```
Enter product name: "HashiCorp Vault"
→ Product Researcher analyzes Vault features
→ Audience Researcher identifies security professionals
→ Campaign Strategist develops go-to-market strategy  
→ Content Creator generates marketing copy
→ Image Generator creates visual concepts
→ System generates actual images via OpenAI
→ QA Validator reviews all content
→ Final campaign package delivered
```

## 🧹 Cleanup & Resource Management

The project includes comprehensive cleanup automation to manage Azure AI resources.

### Cleanup Script (`cleanup.sh`)

The bash wrapper provides easy access to cleanup functionality:

```bash
# Interactive mode (default)
./cleanup.sh

# List all resources without deleting
./cleanup.sh --list

# Delete all agents (with confirmation)
./cleanup.sh --agents

# Delete all agents (skip confirmation)  
./cleanup.sh --agents --confirm

# Delete all threads
./cleanup.sh --all-threads

# Delete specific threads by ID
./cleanup.sh --threads thread_id_1 thread_id_2

# Full cleanup (agents + threads)
./cleanup.sh --full

# Cleanup from session tracking file
./cleanup.sh --session session_tracking.json

# Show help
./cleanup.sh --help
```

### Cleanup Features

- **Agent Management**: List and delete all or specific agents
- **Thread Management**: Clean up conversation threads
- **Session Tracking**: Cleanup based on saved session data
- **Interactive Mode**: Safe cleanup with confirmations
- **Batch Operations**: Efficient bulk deletion with rate limiting
- **Error Handling**: Robust error handling and logging

### Python Cleanup API

Direct access to cleanup functionality:

```python
from cleanup_automation import CleanupAutomation

cleanup = CleanupAutomation()

# List resources
agents = cleanup.list_all_agents()
threads = cleanup.list_all_threads()

# Cleanup operations
cleanup.cleanup_all_agents(confirm=True)
cleanup.cleanup_all_threads(confirm=True)
cleanup.full_cleanup(confirm=True)
```

## 🔧 Configuration

### Agent Configuration (`agent_configs.yaml`)

Defines the specialized agents and their instructions:

```yaml
agents:
  - name: "product_researcher" 
    description: "Gets product details and specifications"
    instructions: "You are TeraSky's Product Research Specialist..."
  
  - name: "audience_researcher"
    description: "Finds relevant audience for the product"
    instructions: "You are TeraSky's Audience Research Expert..."
    
  # ... additional agents
```

### Orchestrator Configuration (`orchestrator_config.yaml`)

Defines the main orchestrator's workflow and coordination logic:

```yaml
orchestrator:
  name: "marketing_campaign_orchestrator"
  instructions: |
    You coordinate specialized agents to create marketing campaigns.
    Follow this workflow:
    1. Use product_researcher function
    2. Use audience_researcher function  
    3. Use campaign_strategist function
    4. Use content_creator function
    5. Use image_generator function
    6. Generate actual images using create_image function
    7. Use qa_validator function
```

## 🔌 OpenAPI Integration

The system integrates directly with OpenAI's Images API using Azure AI's OpenAPI tool functionality:

- **Direct API Access**: No wrapper functions needed
- **Secure Authentication**: Uses Azure AI connection-based auth
- **Standardized Integration**: Follows OpenAPI specifications
- **Image Generation**: Creates actual marketing visuals using DALL-E 3

See `README_OpenAPI_Setup.md` for detailed setup instructions.

## 📊 Output Example

The system generates comprehensive marketing campaigns including:

### Executive Summary
- Campaign objectives and success metrics
- Key strategic recommendations

### Product Analysis  
- Core features and technical specifications
- Value propositions and competitive advantages

### Target Audience
- Primary personas and demographics
- Pain points and communication preferences

### Campaign Strategy
- Multi-channel approach and tactics
- Budget allocation and timeline

### Marketing Content
- Social media posts and messaging
- Email templates and ad copy
- Call-to-action recommendations

### Visual Assets
- Generated marketing images
- Visual concept descriptions
- Brand-consistent design elements

### Quality Assurance
- Content review and recommendations
- Brand compliance verification

## 🔍 Troubleshooting

### Common Issues

**Connection Errors**
```bash
# Verify environment variables
cat .env | grep PROJECT_CONNECTION_STRING

# Test Azure connection
az account show
```

**Agent Creation Failures**
```bash
# Check Azure AI project permissions
# Verify connection string format
# Review agent configuration syntax
```

**Image Generation Issues**
```bash
# Verify OpenAI API key
# Check connection setup in Azure AI Foundry
# Review OpenAPI specification
```

### Debug Mode

Enable verbose logging by setting:
```bash
export AZURE_LOG_LEVEL=DEBUG
```

## 🚀 Advanced Usage

### Custom Agent Development

1. Add agent configuration to `agent_configs.yaml`
2. Update orchestrator workflow in `orchestrator_config.yaml`
3. Restart the application

### Session Tracking

The system can track created resources for easier cleanup:

```python
# Enable session tracking
session_data = {
    'timestamp': datetime.now().isoformat(),
    'agents': [{'id': agent.id, 'name': agent.name} for agent in agents],
    'threads': [{'id': thread.id} for thread in threads]
}

with open('session_tracking.json', 'w') as f:
    json.dump(session_data, f, indent=2)
```

### Bulk Operations

Process multiple products:

```python
products = ['HashiCorp Vault', 'Portworx by Pure', 'Spectro Cloud']
for product in products:
    # Run campaign generation
    # Save results
    # Cleanup resources
```

## 📚 Dependencies

- `azure-ai-projects==1.0.0b10` - Azure AI Agents framework
- `azure-identity==1.23.0` - Azure authentication
- `python-dotenv>=1.0.0` - Environment variable management
- `PyYAML` - Configuration file parsing
- `openai>=1.0.0` - OpenAI API client
- `jsonref>=1.1.0` - JSON reference resolution
- `requests>=2.31.0` - HTTP client library

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Additional Resources

- [Azure AI Agents Documentation](https://learn.microsoft.com/en-us/azure/ai-services/agents/)
- [OpenAI Images API Documentation](https://platform.openai.com/docs/api-reference/images)
- [Azure AI Foundry Portal](https://ai.azure.com)
- [OpenAPI Tool Integration Guide](README_OpenAPI_Setup.md)

---

**TeraSky AI Marketing Campaign Generator** - Powering intelligent marketing automation with Azure AI Agents. 