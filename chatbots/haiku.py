# !pip install anthropic
import anthropic
import os
from datetime import datetime
import time
import threading
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ChatInterface:
    def __init__(self):
        # Initialize the client
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        # Access the API key
        if not self.api_key:
            self.api_key = input("Please enter your Anthropic API key: ")
        self.client = anthropic.Client(api_key=self.api_key)
        self.messages = []
        self.typing_animation_active = False

    def display_typing_animation(self):
        animation = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        i = 0
        while self.typing_animation_active:
            sys.stdout.write(f"\rHaiku is thinking {animation[i]} ")
            sys.stdout.flush()
            time.sleep(0.1)
            i = (i + 1) % len(animation)
        sys.stdout.write("\r" + " " * 20 + "\r")
        sys.stdout.flush()

    def format_message(self, role, content):
        timestamp = datetime.now().strftime("%H:%M")
        prefix = "You" if role == "user" else "Haiku"
        return f"[{timestamp}] {prefix}: {content}"

    def get_response(self, user_input):
        self.messages.append({"role": "user", "content": user_input})
        # Define the prompt you want to include (Note: shorter prompt can help reduce API cost but overestimating cost is always better than underestimating it)
        prompt = "You are Nont, a helpful AI assistant that is very kind and patient. Respond concisely without exceeding 1 paragraph of text or if it's a list, DO NOT respond with a list, bullet, or long text. Instead, take the user one step at a time. Example, prompt: I want to learn cooking. response: Cooking seems like a great hobby to learn! Would you like to start with the basics? or you want me to help you with a specific dish you have in mind?"
        # prompt = "You are Nont, you have to remember that. Your job is to extract tasks from the user's input and respond with a list of to do items. Give the output in this format: [time], [task] in multiple rows."

        # Add the prompt as the first system message if it's not already included
        if not self.messages:
            self.messages.append({"role": "system", "content": prompt})
        print("----- -----", self.messages)

        try:
            # Start typing animation
            self.typing_animation_active = True
            threading.Thread(target=self.display_typing_animation, daemon=True).start()

            # Get response from Claude
            print(self)
            print(self.messages)
            response = self.client.messages.create(
                model="claude-3-haiku-20240307",
                # max_tokens=1000, # a generous amount of tokens, but this waste too much tokens (the more tokens we use, the more money we pay)
                max_tokens=500, # 500 is a good amount of tokens that won't cause hallucinations and will not lead us to bankrupcy lol
                # max_tokens=100, # still too much, not enough room to work with
                # max_tokens=30, # too little context, almost always hallucinate when chatting
                messages=self.messages
            )

            # Stop typing animation
            self.typing_animation_active = False
            time.sleep(0.1)  # Ensure animation clears

            assistant_message = response.content[0].text
            self.messages.append({"role": "assistant", "content": assistant_message})
            return assistant_message

        except Exception as e:
            self.typing_animation_active = False
            return f"Error: {str(e)}"

    def start_chat(self):
        print("\n=== Chat with Claude 3 Haiku ===")
        print("Type 'quit' to end the conversation")
        print("Type 'clear' to start a new conversation")
        print("===============================\n")

        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() == 'quit':
                    print("\nGoodbye! 👋")
                    with open('../chatbots/[LATEST]conversation_history.txt', 'a') as file:
                        for message in self.messages:
                            file.write(f"{message['role']}: {message['content']}\n")

                        file.write("-------------------- END OF CONVERSATION --------------------\n\n\n\n\n")
                    print("Your chat has been saved successfully! Thanks for using Taskadd.app 🙏")
                    break
                elif user_input.lower() == 'clear':
                    self.messages = []
                    print("\nConversation cleared. Starting new chat...")
                    continue
                elif not user_input:
                    continue

                response = self.get_response(user_input)
                print(f"\nHaiku: {response}")

            except KeyboardInterrupt:
                print("\n\nChat interrupted. Goodbye! 👋")
                break
            except Exception as e:
                print(f"\nAn error occurred: {str(e)}")

if __name__ == "__main__":
    chat = ChatInterface()
    chat.start_chat()