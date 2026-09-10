import time

def mock_ai_response(messages):
    """
    Simulates an AI generating a response based on the conversation history (context).
    This function demonstrates how context can influence the AI's reply.
    """
    last_user_message = ""
    if messages:
        # Find the last user message to base the immediate response on
        for msg in reversed(messages):
            if msg["role"] == "user":
                last_user_message = msg["content"].lower()
                break

    # Simple context-aware logic
    # The AI's response changes based on keywords in the current message AND previous messages.
    if "hello" in last_user_message or "hi" in last_user_message:
        return "Hello there! How can I assist you today?"
    elif "weather" in last_user_message:
        # Check for previous messages about location or time for more context
        for msg in reversed(messages[:-1]): # Look at previous messages, excluding the current one
            if msg["role"] == "user" and "tomorrow" in msg["content"].lower():
                # Context: User asked about weather, and previously mentioned 'tomorrow'
                return "The weather tomorrow is expected to be sunny with a high of 25°C."
            if msg["role"] == "user" and "istanbul" in msg["content"].lower():
                # Context: User asked about weather, and previously mentioned 'Istanbul'
                return "The current weather in Istanbul is partly cloudy, 18°C."
        return "I can tell you about the weather. Where are you interested in, or for when?"
    elif "capital" in last_user_message:
        # Check for previous country mentions to provide a more specific answer
        for msg in reversed(messages[:-1]):
            if msg["role"] == "user":
                if "france" in msg["content"].lower():
                    # Context: User asked about capital, and previously mentioned 'France'
                    return "The capital of France is Paris."
                if "germany" in msg["content"].lower():
                    # Context: User asked about capital, and previously mentioned 'Germany'
                    return "The capital of Germany is Berlin."
        return "Which country's capital are you asking about?"
    elif "joke" in last_user_message:
        # Keep track of jokes told to tell a different one, demonstrating memory/state
        jokes_told = [msg["content"] for msg in messages if msg["role"] == "assistant" and "joke" in msg["content"].lower()]
        if "Why don't scientists trust atoms?" not in jokes_told:
            return "Why don't scientists trust atoms? Because they make up everything!"
        else:
            # Context: A joke was already told, so tell a different one
            return "What do you call a fake noodle? An impasta!"
    elif "thank you" in last_user_message or "thanks" in last_user_message:
        return "You're welcome! Is there anything else I can help with?"
    elif "bye" in last_user_message or "goodbye" in last_user_message:
        return "Goodbye! Have a great day!"
    else:
        # Default response, potentially using the last message for generic follow-up
        if last_user_message:
            return f"You mentioned '{last_user_message}'. Can you elaborate or ask something else?"
        return "I'm not sure how to respond to that. Could you please rephrase or ask something different?"

def main():
    print("Welcome to the Context-Aware Chat Bot!")
    print("Type 'bye' to exit.")
    print("-" * 40)

    chat_history = [] # This list stores the entire conversation context

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == 'bye':
            print("Bot: Goodbye!")
            break

        # Add user's message to the chat history, building the context
        chat_history.append({"role": "user", "content": user_input})

        # Simulate AI thinking time
        time.sleep(0.5)

        # Get AI's response, passing the entire chat history for context.
        # This is analogous to how Open WebUI would send the conversation history
        # to an underlying LLM for context-aware generation.
        ai_response = mock_ai_response(chat_history)

        # Add AI's response to the chat history, further enriching the context
        chat_history.append({"role": "assistant", "content": ai_response})

        print(f"Bot: {ai_response}")
        print("-" * 40)

if __name__ == "__main__":
    main()
