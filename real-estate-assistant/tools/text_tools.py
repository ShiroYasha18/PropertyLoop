#tools/text_tools.py
def extract_location(text: str) -> str:
    """
    Extract location information from text
    """
    return text

def get_conversation_context(messages: list) -> str:
    """
    Build context from previous messages
    Args:
        messages (list): List of message dictionaries with 'role' and 'content' keys
    Returns:
        str: Formatted conversation context
    """
    context = []
    # Get last 5 messages for recent context
    for message in messages[-5:]:
        role = "User" if message["role"] == "user" else "Assistant"
        content = message["content"]
        context.append(f"{role}: {content}")
    
    return "\n".join(context)

def build_query_context(current_query: str, conversation_history: list) -> str:
    """
    Combine current query with conversation history
    Args:
        current_query (str): Current user input
        conversation_history (list): List of previous messages
    Returns:
        str: Combined context string
    """
    history = get_conversation_context(conversation_history)
    return f"Current Query: {current_query}\n\nPrevious Context:\n{history}"

# Remove or comment out location_tool if it's not implemented