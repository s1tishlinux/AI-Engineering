# Enhanced AI Agent Chatbot

import re
from typing import Dict, List, Optional, Callable

class EnhancedAgentChatbot:
    def __init__(self):
        self.memory: Dict[str, str] = {}
        self.tools: Dict[str, Callable] = {}
        self.conversation_history: List[str] = []
        self.context_window: int = 3  # Number of previous turns to consider

    def add_to_memory(self, key: str, value: str) -> None:
        """Store information in the agent's memory with validation"""
        if not key or not value:
            raise ValueError("Key and value must not be empty")
        self.memory[key.lower()] = value

    def recall_from_memory(self, query: str) -> Optional[str]:
        """Context-aware memory retrieval using semantic matching"""
        query = query.lower()
        # Simple semantic matching - would use embeddings in a real implementation
        for key, value in self.memory.items():
            if query in key or key in query:
                return value
        return None

    def register_tool(self, name: str, function: Callable, description: str) -> None:
        """Register a tool with a description for natural language understanding"""
        if not name or not callable(function):
            raise ValueError("Invalid tool registration")
        self.tools[name.lower()] = {
            "function": function,
            "description": description
        }

    def find_tool_by_description(self, description: str) -> Optional[str]:
        """Find a tool by its description using natural language matching"""
        description = description.lower()
        for name, tool_info in self.tools.items():
            if description in tool_info["description"].lower():
                return name
        return None

    def process_input(self, user_input: str) -> str:
        """Process user input with multi-turn conversation handling"""
        self.conversation_history.append(f"User: {user_input}")

        # Check for tool requests
        tool_match = re.search(r"(?:use|run|execute) (.+?)(?: tool)?(?: with (.+))?", user_input, re.IGNORECASE)
        if tool_match:
            tool_name = tool_match.group(1).lower()
            args_str = tool_match.group(2)
            return self._handle_tool_request(tool_name, args_str)

        # Check for memory requests
        memory_match = re.search(r"(?:remember|recall|what is|tell me about) (.+)", user_input, re.IGNORECASE)
        if memory_match:
            query = memory_match.group(1)
            recalled = self.recall_from_memory(query)
            if recalled:
                response = f"I remember: {recalled}"
            else:
                response = f"I don't have information about {query} in my memory."
            self.conversation_history.append(f"Agent: {response}")
            return response

        # Default response with context from conversation history
        context = "\n".join(self.conversation_history[-self.context_window:])
        response = f"I'm here to help. Based on our conversation:\n{context}\nWhat would you like to know or do next?"
        self.conversation_history.append(f"Agent: {response}")
        return response

    def _handle_tool_request(self, tool_name: str, args_str: Optional[str]) -> str:
        """Handle tool requests with argument parsing"""
        # Try to find the tool by name first
        tool_info = self.tools.get(tool_name)
        if not tool_info:
            # If not found, try to find by description
            tool_name = self.find_tool_by_description(tool_name)
            if not tool_name:
                return f"I don't have a tool named {tool_name}."
            tool_info = self.tools[tool_name]

        # Parse arguments
        args = []
        if args_str:
            # Simple argument parsing - would use more sophisticated parsing in a real implementation
            args = [arg.strip() for arg in args_str.split(",")]

        try:
            # Convert string arguments to appropriate types
            converted_args = []
            for arg in args:
                if arg.isdigit():
                    converted_args.append(int(arg))
                elif arg.replace(".", "", 1).isdigit():
                    converted_args.append(float(arg))
                else:
                    converted_args.append(arg)

            result = tool_info["function"](*converted_args)
            response = f"Tool {tool_name} executed with result: {result}"
        except Exception as e:
            response = f"Error executing tool {tool_name}: {str(e)}"

        self.conversation_history.append(f"Agent: {response}")
        return response

# Example usage
if __name__ == "__main__":
    agent = EnhancedAgentChatbot()

    # Add some initial memory
    agent.add_to_memory("name", "Claude")
    agent.add_to_memory("purpose", "Help with AI engineering")
    agent.add_to_memory("creator", "Anthropic")

    # Register tools with descriptions
    def calculate(a: float, b: float) -> float:
        return a + b

    def weather(city: str) -> str:
        # In a real implementation, this would call a weather API
        return f"Weather in {city}: Sunny, 25°C"

    agent.register_tool("calculator", calculate, "Performs basic arithmetic operations")
    agent.register_tool("weather", weather, "Provides weather information for a given city")

    # Test the agent
    print(agent.process_input("What's your name?"))
    print(agent.process_input("What do you do?"))
    print(agent.process_input("Who created you?"))
    print(agent.process_input("Use calculator tool with 5, 3"))
    print(agent.process_input("Execute weather for New York"))
    print(agent.process_input("Tell me about your purpose"))
    print(agent.process_input("What was our previous conversation about?"))
