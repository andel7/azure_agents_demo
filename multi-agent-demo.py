import os
import yaml
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import ConnectedAgentTool, MessageRole, OpenApiTool, OpenApiConnectionAuthDetails, OpenApiConnectionSecurityScheme
import jsonref
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
import json
load_dotenv()

# Load agent configurations from YAML file
def load_agent_configs(config_file="agent_configs.yaml"):
    """
    Load agent configurations from a YAML file
    """
    try:
        with open(config_file, 'r', encoding='utf-8') as file:
            config_data = yaml.safe_load(file)
            return config_data['agents']
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_file}' not found.")
        raise
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        raise
    except KeyError:
        print("Error: 'agents' key not found in configuration file.")
        raise

def load_orchestrator_config(config_file="orchestrator_config.yaml"):
    """
    Load orchestrator configuration from a YAML file
    """
    try:
        with open(config_file, 'r', encoding='utf-8') as file:
            config_data = yaml.safe_load(file)
            return config_data['orchestrator']
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_file}' not found.")
        raise
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        raise
    except KeyError:
        print("Error: 'orchestrator' key not found in configuration file.")
        raise

# Load agent configurations
AGENT_CONFIGS = load_agent_configs()
ORCHESTRATOR_CONFIG = load_orchestrator_config()

def create_agent_and_tool(project_client, config):
    """
    Function to create an agent and its corresponding connected agent tool
    """
    # Create agent WITHOUT file tools - only the orchestrator needs them
    agent = project_client.agents.create_agent(
        model="gpt-4o",
        name=config["name"],
        instructions=config["instructions"],
        # No tools for individual agents - they just provide focused responses
    )
    
    connected_tool = ConnectedAgentTool(
        id=agent.id, 
        name=config["name"], 
        description=config["description"]
    )
    
    return agent, connected_tool

def delete_agents(project_client, agents):
    """
    Function to delete multiple agents
    """
    for agent in agents:
        project_client.agents.delete_agent(agent.id)
        print(f"Deleted agent: {agent.name}")

# Initialize the client object
project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=os.environ["PROJECT_CONNECTION_STRING"]
)

# Load the OpenAPI specification for Replicate Imagen-4 API
with open("replicate_imagen4_spec_fixed.json", "r") as f:
    replicate_imagen4_spec = jsonref.loads(f.read())

# Create or use existing connection for Replicate API
# You can override this with an environment variable
connection_id = os.getenv("REPLICATE_CONNECTION_ID", "/subscriptions/5d70695f-e89b-49af-a96a-71cfbef69887/resourceGroups/lev-test/providers/Microsoft.MachineLearningServices/workspaces/lev-7636/connections/replicate-api-connection")
print(f"🔗 Using connection ID: {connection_id}")

try:
    # Try to create a connection if it doesn't exist
    from azure.ai.projects.models import ConnectionAuthenticationType, CustomKeyAuthConfiguration
    
    api_key = os.getenv("REPLICATE_API_TOKEN")
    if api_key:
        # Create connection configuration
        connection_config = {
            "type": "custom_keys",
            "name": connection_id,
            "properties": {
                "Authorization": f"Bearer {api_key}"
            }
        }
        
        # Note: Connection creation via SDK might not be available
        # Fall back to expecting manual connection setup
        print(f"Using connection: {connection_id}")
        
except Exception as e:
    print(f"Note: Please ensure connection '{connection_id}' exists in Azure AI Foundry")
    print(f"Connection should have key 'Authorization' with value 'Bearer YOUR_REPLICATE_API_TOKEN'")

# Use connection-based authentication
auth = OpenApiConnectionAuthDetails(
    security_scheme=OpenApiConnectionSecurityScheme(
        connection_id=connection_id
    )
)

# Create OpenApiTool for image generation
image_generation_tool = OpenApiTool(
    name="generate_image",
    spec=replicate_imagen4_spec,
    description="Generate high-quality images using Google's Imagen-4 model on Replicate. Use this tool when the image_generator agent provides visual concepts and you need to create actual images. The tool accepts prompts and returns URLs to generated images.",
    auth=auth
)

with project_client:
    # Create agents and connected tools using loop
    agents = []
    connected_tools = []
    
    for config in AGENT_CONFIGS:
        agent, connected_tool = create_agent_and_tool(project_client, config)
        agents.append(agent)
        connected_tools.append(connected_tool)
        print(f"Created agent: {agent.name} (ID: {agent.id})")

    # Create the "main" agent that will use all connected agents
    # Get connected agent tools definitions for the agent creation
    connected_agent_tools = []
    for tool in connected_tools:
        connected_agent_tools.extend(tool.definitions)
    
    marketing_campaign_orchestrator = project_client.agents.create_agent(
        model="gpt-4o",
        name=ORCHESTRATOR_CONFIG["name"],
        instructions=ORCHESTRATOR_CONFIG["instructions"],
        tools=connected_agent_tools + image_generation_tool.definitions,  # Include image generation tool
    )

    print(f"Created main agent, ID: {marketing_campaign_orchestrator.id}")

    # Get product name from user input
    product_name = input("Please enter the product name for the marketing campaign: ")
    print(f"Generating campaign for: {product_name}")

    # Create a thread and add a message to it
    thread = project_client.agents.create_thread()
    print(f"Created thread, ID: {thread.id}")

    # Create message to thread
    message = project_client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content=f"Generate campaign strategy, content for {product_name}",
    )
    print(f"Created message, ID: {message.id}")

    # Create a run with connected agents
    run = project_client.agents.create_and_process_run(
        thread_id=thread.id, 
        agent_id=marketing_campaign_orchestrator.id
    )
    print(f"Run finished with status: {run.status}")

    if run.status == "failed":
        print(f"Run failed: {run.last_error}")

    # Print the Agent's response message with optional citation
    messages = project_client.agents.list_messages(thread_id=thread.id)
    for message in messages.data:
        if message.role == "assistant":
            for content in message.content:
                if hasattr(content, 'text') and hasattr(content.text, 'value'):
                    print(f"Agent response: {content.text.value}")
            # Handle citations if they exist
            if hasattr(message, 'url_citation_annotations') and message.url_citation_annotations:
                for annotation in message.url_citation_annotations:
                    print(f"URL Citation: [{annotation.url_citation.title}]({annotation.url_citation.url})")
            break  # Get the first agent message

    # Delete the main agent
    #project_client.agents.delete_agent(main_agent.id)
    #print("Deleted main agent")

    # Delete all connected agents using the function and loop
    #delete_agents(project_client, agents)