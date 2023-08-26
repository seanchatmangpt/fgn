import openai

# Store API Key
openai.api_key = 'api_key'

# Define chat completion model
model = "gpt-3.5-turbo"

# Prepare system message
system = "You are a helpful assistant."

# Prepare user message
user = "Translate the following English text to French: '{'Hello, world!'}'"

# Create the message array
messages = [
    {"role": "system", "content": system},
    {"role": "user", "content": user},
]

# Use OpenAI's `ChatCompletion` to generate a conversation based on the given messages and model
response = openai.ChatCompletion.create(
  model=model,
  messages=messages,
)

# Print the assistant's message
print(response['choices'][0]['message']['content'])
