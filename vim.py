import os
import google.generativeai as genai

def main():
    # Configure the Gemini API key
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    genai.configure(api_key=GOOGLE_API_KEY)
 
    # Initialize the model
    model = genai.GenerativeModel('gemini-1.5-flash')
    chat_session = model.start_chat(history=[])

    # Initial system instructions
    sys_instructions = "You are a helpful assistant."
    try:
        chat_session.send_message(sys_instructions)
    except Exception as e:
        print(f"Error sending system instructions: {e}")
        return

    # Keep taking prompts and generating responses
    while True:
        prompt = input("Enter your prompt (or type 'exit' to quit): ")
        if prompt.lower() == 'exit':
            print("Goodbye!")
            break

        try:
            response = chat_session.send_message(prompt)
            print("Response:", response.text.strip())
        except Exception as e:
            print(f"Error generating response: {e}")

if __name__ == "__main__":
    main()
