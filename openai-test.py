import os
from openai import OpenAI
client = OpenAI()

# Ensure the API key is set in the environment
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

# Set the OpenAI API key
OpenAI.api_key = api_key

# Create a chat completion with the correct method
completion = client.chat.completions.create(
    model="gpt-4o-mini",  # Model name
    messages=[  # Conversation setup
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a haiku about recursion in programming."}
    ]
)

# Extracting and printing the response
print(completion.choices[0].message.content)

