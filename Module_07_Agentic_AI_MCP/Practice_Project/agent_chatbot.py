# Basic AI Agent Chatbot

class AgentChatbot:
    def __init__(self):
        self.memory = {}
        self.tools = {}
        self.conversation_history = []

    def add_to_memory(self, key, value):
        """Store information in the agent's memory"""
        self.memory[key] = value

    def recall_from_memory(self, key):
        """Retrieve information from the agent's memory"""
        return self.memory.get(key, None)

    def register_tool(self, name, function):
        """Register a tool that the agent can use"""
        self.tools[name] = function

    def use_tool(self, tool_name, *args):
        """Use a registered tool with the given arguments"""
        if tool_name in self.tools:
            return self.tools[tool_name](*args)
        return None

    def process_input(self, user_input):
        """Process user input and generate a response"""
        # Simple reasoning: check if input matches any memory keys
        for key in self.memory:
            if key.lower() in user_input.lower():
                return f"I remember: {self.memory[key]}"

        # If no memory match, use a default response
        self.conversation_history.append(user_input)
        return "I'm here to help. What would you like to know or do?"

# Example usage
if __name__ == "__main__":
    agent = AgentChatbot()

    # Add some initial memory
    agent.add_to_memory("name", "Claude")
    agent.add_to_memory("purpose", "Help with AI engineering")

    # Register a simple tool
    def calculate(a, b):
        return a + b

    agent.register_tool("calculator", calculate)

    # Test the agent
    print(agent.process_input("What's your name?"))
    print(agent.process_input("What do you do?"))
    print(agent.process_input("Calculate 5 plus 3"))
    print(agent.use_tool("calculator", 5, 3))
