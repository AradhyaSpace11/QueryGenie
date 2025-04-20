import google.generativeai as genai

# Configure the Gemini API with your API key
API_KEY = ""
genai.configure(api_key=API_KEY)

# Initialize the Gemini model
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

# Function to handle chat history and responses
def chat_with_gemini(user_input, chat_history):
    """
    Sends a message to the Gemini API, including chat history, and returns the response.

    Args:
        user_input (str): The latest message from the user.
        chat_history (list): List of previous messages in the conversation.

    Returns:
        response_text (str): The response from Gemini.
    """
    try:
        # Start a new chat session
        chat = gemini_model.start_chat()

        # Create the prompt with chat history
        prompt = "\n".join(chat_history) + f"\nUser: {user_input}\n"

        # Send the message to Gemini
        response = chat.send_message(prompt)
        response_text = response.text

        # Add the new user input and response to the chat history
        chat_history.append(f"User: {user_input}")
        chat_history.append(f"Gemini: {response_text}")

        return response_text

    except Exception as e:
        return f"Error querying Gemini: {str(e)}"


# Example Usage
if __name__ == "__main__":
    chat_history = []  # Initialize an empty chat history

    print("Start chatting with Gemini (type 'exit' to quit).")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        # Get the response from Gemini
        response = chat_with_gemini(user_input, chat_history)

        # Display the response
        print(f"Gemini: {response}")
