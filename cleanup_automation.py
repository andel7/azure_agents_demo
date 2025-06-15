#!/usr/bin/env python3
"""
Cleanup Automation for AI Tour 2025 Project
Cleans up all agents and threads created in the Azure AI project.
"""

import os
import sys
import time
import json
from typing import List, Any
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class CleanupAutomation:
    """Automation class for cleaning up agents and threads"""
    
    def __init__(self):
        """Initialize the cleanup automation with Azure AI client"""
        try:
            self.project_client = AIProjectClient.from_connection_string(
                credential=DefaultAzureCredential(),
                conn_str=os.environ["PROJECT_CONNECTION_STRING"]
            )
            print("✅ Successfully connected to Azure AI Project")
        except KeyError:
            print("❌ Error: PROJECT_CONNECTION_STRING environment variable not found")
            print("   Please make sure your .env file contains the connection string")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error connecting to Azure AI Project: {e}")
            sys.exit(1)
    
    def list_all_agents(self) -> List[Any]:
        """List all agents in the project"""
        try:
            agents = self.project_client.agents.list_agents()
            # Agents are returned in the 'data' attribute as a list of dictionaries
            return agents.data if hasattr(agents, 'data') else []
        except Exception as e:
            print(f"❌ Error listing agents: {e}")
            return []
    
    def list_all_threads(self) -> List[Any]:
        """List all threads in the project"""
        try:
            threads = self.project_client.agents.list_threads()
            # Threads are returned in the 'data' attribute as a list of thread objects
            return threads.data if hasattr(threads, 'data') else []
        except Exception as e:
            print(f"❌ Error listing threads: {e}")
            return []
    
    def delete_agent(self, agent_id: str, agent_name: str = None) -> bool:
        """Delete a single agent by ID"""
        try:
            self.project_client.agents.delete_agent(agent_id)
            name_info = f" ({agent_name})" if agent_name else ""
            print(f"✅ Deleted agent: {agent_id}{name_info}")
            return True
        except Exception as e:
            print(f"❌ Error deleting agent {agent_id}: {e}")
            return False
    
    def delete_thread(self, thread_id: str) -> bool:
        """Delete a single thread by ID"""
        try:
            self.project_client.agents.delete_thread(thread_id)
            print(f"✅ Deleted thread: {thread_id}")
            return True
        except Exception as e:
            print(f"❌ Error deleting thread {thread_id}: {e}")
            return False
    
    def cleanup_all_agents(self, confirm: bool = False) -> int:
        """Delete all agents in the project"""
        agents = self.list_all_agents()
        
        if not agents:
            print("ℹ️  No agents found to delete")
            return 0
        
        print(f"\n📋 Found {len(agents)} agent(s) to delete:")
        for agent in agents:
            print(f"   - {agent['id']} ({agent['name']})")
        
        if not confirm:
            response = input(f"\n⚠️  Are you sure you want to delete ALL {len(agents)} agents? (yes/no): ")
            if response.lower() not in ['yes', 'y']:
                print("❌ Cleanup cancelled by user")
                return 0
        
        print("\n🧹 Starting agent cleanup...")
        deleted_count = 0
        
        for agent in agents:
            if self.delete_agent(agent['id'], agent['name']):
                deleted_count += 1
            time.sleep(0.5)  # Small delay to avoid rate limiting
        
        print(f"\n✅ Cleanup complete! Deleted {deleted_count}/{len(agents)} agents")
        return deleted_count
    
    def cleanup_specific_threads(self, thread_ids: List[str], confirm: bool = False) -> int:
        """Delete specific threads by their IDs"""
        if not thread_ids:
            print("ℹ️  No thread IDs provided")
            return 0
        
        print(f"\n📋 Preparing to delete {len(thread_ids)} thread(s):")
        for thread_id in thread_ids:
            print(f"   - {thread_id}")
        
        if not confirm:
            response = input(f"\n⚠️  Are you sure you want to delete these {len(thread_ids)} threads? (yes/no): ")
            if response.lower() not in ['yes', 'y']:
                print("❌ Cleanup cancelled by user")
                return 0
        
        print("\n🧹 Starting thread cleanup...")
        deleted_count = 0
        
        for thread_id in thread_ids:
            if self.delete_thread(thread_id):
                deleted_count += 1
            time.sleep(0.5)  # Small delay to avoid rate limiting
        
        print(f"\n✅ Thread cleanup complete! Processed {deleted_count}/{len(thread_ids)} threads")
        return deleted_count
    
    def cleanup_all_threads(self, confirm: bool = False) -> int:
        """Delete all threads in the project"""
        threads = self.list_all_threads()
        
        if not threads:
            print("ℹ️  No threads found to delete")
            return 0
        
        print(f"\n📋 Found {len(threads)} thread(s) to delete:")
        for thread in threads:
            thread_id = thread.id if hasattr(thread, 'id') else thread['id']
            created_at = thread.created_at if hasattr(thread, 'created_at') else thread.get('created_at', 'unknown')
            print(f"   - {thread_id} (created: {created_at})")
        
        if not confirm:
            response = input(f"\n⚠️  Are you sure you want to delete ALL {len(threads)} threads? (yes/no): ")
            if response.lower() not in ['yes', 'y']:
                print("❌ Cleanup cancelled by user")
                return 0
        
        print("\n🧹 Starting thread cleanup...")
        deleted_count = 0
        
        for thread in threads:
            thread_id = thread.id if hasattr(thread, 'id') else thread['id']
            if self.delete_thread(thread_id):
                deleted_count += 1
            time.sleep(0.5)  # Small delay to avoid rate limiting
        
        print(f"\n✅ Cleanup complete! Deleted {deleted_count}/{len(threads)} threads")
        return deleted_count
    
    def load_session_data(self, filename="session_tracking.json") -> dict:
        """Load session tracking data"""
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"ℹ️  No session tracking file found: {filename}")
            return {}
        except json.JSONDecodeError as e:
            print(f"❌ Error reading session file: {e}")
            return {}
    
    def cleanup_from_session_file(self, filename="session_tracking.json", confirm: bool = False) -> dict:
        """Cleanup resources based on session tracking file"""
        session_data = self.load_session_data(filename)
        
        if not session_data:
            print("❌ No session data found to cleanup")
            return {'agents_deleted': 0, 'threads_deleted': 0, 'success': False}
        
        print(f"📋 Found session data from: {session_data.get('timestamp', 'unknown time')}")
        
        results = {
            'agents_deleted': 0,
            'threads_deleted': 0,
            'success': False
        }
        
        # Get agent and thread IDs from session data
        agent_ids = [agent['id'] for agent in session_data.get('agents', [])]
        thread_ids = [thread['id'] for thread in session_data.get('threads', [])]
        
        if not agent_ids and not thread_ids:
            print("ℹ️  No agents or threads found in session data")
            return results
        
        print(f"\n📊 Session contains:")
        print(f"   • {len(agent_ids)} agent(s)")
        print(f"   • {len(thread_ids)} thread(s)")
        
        if not confirm:
            response = input(f"\n⚠️  Delete all resources from this session? (yes/no): ")
            if response.lower() not in ['yes', 'y']:
                print("❌ Cleanup cancelled by user")
                return results
        
        # Delete agents from session
        if agent_ids:
            print("\n🧹 Cleaning up agents from session...")
            for agent_data in session_data.get('agents', []):
                if self.delete_agent(agent_data['id'], agent_data.get('name')):
                    results['agents_deleted'] += 1
                time.sleep(0.5)
        
        # Delete threads from session
        if thread_ids:
            print("\n🧹 Cleaning up threads from session...")
            for thread_data in session_data.get('threads', []):
                if self.delete_thread(thread_data['id']):
                    results['threads_deleted'] += 1
                time.sleep(0.5)
        
        results['success'] = True
        print(f"\n✅ Session cleanup complete!")
        print(f"   • Agents deleted: {results['agents_deleted']}/{len(agent_ids)}")
        print(f"   • Threads processed: {results['threads_deleted']}/{len(thread_ids)}")
        
        return results
    
    def full_cleanup(self, confirm: bool = False) -> dict:
        """Perform a complete cleanup of all agents and threads"""
        print("🚀 Starting full cleanup automation...")
        
        results = {
            'agents_deleted': 0,
            'threads_deleted': 0,
            'success': False
        }
        
        try:
            # Cleanup agents
            agents_deleted = self.cleanup_all_agents(confirm=confirm)
            results['agents_deleted'] = agents_deleted
            
            # Cleanup threads
            threads_deleted = self.cleanup_all_threads(confirm=confirm)
            results['threads_deleted'] = threads_deleted
            
            results['success'] = True
            print("\n🎉 Full cleanup automation completed successfully!")
            
        except Exception as e:
            print(f"\n❌ Error during full cleanup: {e}")
            results['success'] = False
        
        return results

def main():
    """Main function for command-line usage"""
    print("🤖 AI Tour 2025 - Cleanup Automation")
    print("====================================")
    
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description="Cleanup automation for agents and threads")
    parser.add_argument('--agents', action='store_true', help='Delete all agents')
    parser.add_argument('--threads', nargs='*', help='Delete specific threads by ID (or all if no IDs provided)')
    parser.add_argument('--all-threads', action='store_true', help='Delete all threads')
    parser.add_argument('--full', action='store_true', help='Full cleanup (agents + threads)')
    parser.add_argument('--session', type=str, help='Cleanup from session tracking file')
    parser.add_argument('--confirm', action='store_true', help='Skip confirmation prompts')
    parser.add_argument('--list-only', action='store_true', help='Only list agents/threads without deleting')
    
    args = parser.parse_args()
    
    # Initialize cleanup automation
    cleanup = CleanupAutomation()
    
    if args.list_only:
        # List agents and threads without deleting
        print("\n📋 Current agents:")
        agents = cleanup.list_all_agents()
        if agents:
            for agent in agents:
                print(f"   - {agent['id']} ({agent['name']})")
        else:
            print("   No agents found")
        
        print("\n📋 Current threads:")
        threads = cleanup.list_all_threads()
        if threads:
            for thread in threads:
                thread_id = thread.id if hasattr(thread, 'id') else thread['id']
                created_at = thread.created_at if hasattr(thread, 'created_at') else thread.get('created_at', 'unknown')
                print(f"   - {thread_id} (created: {created_at})")
        else:
            print("   No threads found")
        return
    
    if args.full:
        # Full cleanup
        cleanup.full_cleanup(confirm=args.confirm)
    elif args.agents:
        # Cleanup only agents
        cleanup.cleanup_all_agents(confirm=args.confirm)
    elif args.all_threads:
        # Cleanup all threads
        cleanup.cleanup_all_threads(confirm=args.confirm)
    elif args.threads is not None:
        # Cleanup specific threads or all if no IDs provided
        if args.threads:
            cleanup.cleanup_specific_threads(args.threads, confirm=args.confirm)
        else:
            cleanup.cleanup_all_threads(confirm=args.confirm)
    elif args.session:
        # Cleanup from session file
        cleanup.cleanup_from_session_file(args.session, confirm=args.confirm)
    else:
        # Interactive mode
        print("\nSelect cleanup option:")
        print("1. Delete all agents")
        print("2. Delete all threads")
        print("3. Delete specific threads")
        print("4. Full cleanup (agents + threads)")
        print("5. Cleanup from session file")
        print("6. List current resources")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ")
        
        if choice == '1':
            cleanup.cleanup_all_agents()
        elif choice == '2':
            cleanup.cleanup_all_threads()
        elif choice == '3':
            thread_ids = input("Enter thread IDs separated by spaces: ").split()
            if thread_ids and thread_ids[0]:
                cleanup.cleanup_specific_threads(thread_ids)
            else:
                print("❌ No thread IDs provided")
        elif choice == '4':
            cleanup.full_cleanup()
        elif choice == '5':
            filename = input("Enter session file path (or press Enter for 'session_tracking.json'): ").strip()
            if not filename:
                filename = "session_tracking.json"
            cleanup.cleanup_from_session_file(filename)
        elif choice == '6':
            agents = cleanup.list_all_agents()
            if agents:
                print(f"\n📋 Found {len(agents)} agent(s):")
                for agent in agents:
                    print(f"   - {agent['id']} ({agent['name']})")
            else:
                print("\n📋 No agents found")
            
            threads = cleanup.list_all_threads()
            if threads:
                print(f"\n📋 Found {len(threads)} thread(s):")
                for thread in threads:
                    thread_id = thread.id if hasattr(thread, 'id') else thread['id']
                    created_at = thread.created_at if hasattr(thread, 'created_at') else thread.get('created_at', 'unknown')
                    print(f"   - {thread_id} (created: {created_at})")
            else:
                print("\n📋 No threads found")
        elif choice == '7':
            print("👋 Goodbye!")
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main() 