
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Get Groq API key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found. Check your .env file.")

# Initialize Groq client
client = Groq(api_key=api_key)


# Reusable LLM function
def ask_llm(prompt):

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


# First LLM test required by mentor
if __name__ == "__main__":

    question = "What is a VPN?"

    print("\nQuestion:", question)

    answer = ask_llm(question)

    print("\nGroq AI Response:")
    print(answer)
