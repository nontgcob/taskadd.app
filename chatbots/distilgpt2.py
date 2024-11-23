import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
model = AutoModelForCausalLM.from_pretrained("distilgpt2")

# Function to generate a response from the chatbot
def generate_response(prompt):
    # Add a prompting stage
    prompt = f"You are an excited chatbot designed to help guide user through their journey to achiving their goals. {prompt}"
    
    inputs = tokenizer(prompt, return_tensors="pt")
    # Create an attention mask
    attention_mask = inputs['attention_mask']
    # Generate the response with attention mask and pad_token_id
    outputs = model.generate(inputs.input_ids, attention_mask=attention_mask, max_length=150, num_return_sequences=1, pad_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

# Simple chat loop
print("DistilGPT-2 Chatbot (Type 'quit' to exit)")
while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        print("Quitting chat. Goodbye!")
        break
    response = generate_response(user_input)
    print(f"DistilGPT-2: {response}")